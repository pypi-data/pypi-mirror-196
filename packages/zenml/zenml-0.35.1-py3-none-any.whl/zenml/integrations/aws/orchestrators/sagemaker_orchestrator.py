#  Copyright (c) ZenML GmbH 2022. All Rights Reserved.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at:
#
#       https://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
#  or implied. See the License for the specific language governing
#  permissions and limitations under the License.
"""Implementation of the SageMaker orchestrator."""

import os
from typing import TYPE_CHECKING, Dict, Optional, Tuple, Type, cast
from uuid import UUID

import sagemaker
from sagemaker.workflow.execution_variables import ExecutionVariables
from sagemaker.workflow.pipeline import Pipeline
from sagemaker.workflow.steps import ProcessingStep

from zenml.config.base_settings import BaseSettings
from zenml.entrypoints import StepEntrypointConfiguration
from zenml.enums import StackComponentType
from zenml.integrations.aws.flavors.sagemaker_orchestrator_flavor import (
    SagemakerOrchestratorConfig,
    SagemakerOrchestratorSettings,
)
from zenml.logger import get_logger
from zenml.metadata.metadata_types import MetadataType
from zenml.orchestrators import ContainerizedOrchestrator
from zenml.orchestrators.utils import get_orchestrator_run_name
from zenml.stack import StackValidator

if TYPE_CHECKING:
    from zenml.models.pipeline_deployment_models import (
        PipelineDeploymentResponseModel,
    )
    from zenml.stack import Stack

ENV_ZENML_SAGEMAKER_RUN_ID = "ZENML_SAGEMAKER_RUN_ID"
MAX_POLLING_ATTEMPTS = 100
POLLING_DELAY = 30

logger = get_logger(__name__)


class SagemakerOrchestrator(ContainerizedOrchestrator):
    """Orchestrator responsible for running pipelines on Sagemaker."""

    @property
    def config(self) -> SagemakerOrchestratorConfig:
        """Returns the `SagemakerOrchestratorConfig` config.

        Returns:
            The configuration.
        """
        return cast(SagemakerOrchestratorConfig, self._config)

    @property
    def validator(self) -> Optional[StackValidator]:
        """Validates the stack.

        In the remote case, checks that the stack contains a container registry,
        image builder and only remote components.

        Returns:
            A `StackValidator` instance.
        """

        def _validate_remote_components(
            stack: "Stack",
        ) -> Tuple[bool, str]:
            for component in stack.components.values():
                if not component.config.is_local:
                    continue

                return False, (
                    f"The Sagemaker orchestrator runs pipelines remotely, "
                    f"but the '{component.name}' {component.type.value} is "
                    "a local stack component and will not be available in "
                    "the Sagemaker step.\nPlease ensure that you always "
                    "use non-local stack components with the Sagemaker "
                    "orchestrator."
                )

            return True, ""

        return StackValidator(
            required_components={
                StackComponentType.CONTAINER_REGISTRY,
                StackComponentType.IMAGE_BUILDER,
            },
            custom_validation_function=_validate_remote_components,
        )

    def get_orchestrator_run_id(self) -> str:
        """Returns the run id of the active orchestrator run.

        Important: This needs to be a unique ID and return the same value for
        all steps of a pipeline run.

        Returns:
            The orchestrator run id.

        Raises:
            RuntimeError: If the run id cannot be read from the environment.
        """
        try:
            return os.environ[ENV_ZENML_SAGEMAKER_RUN_ID]
        except KeyError:
            raise RuntimeError(
                "Unable to read run id from environment variable "
                f"{ENV_ZENML_SAGEMAKER_RUN_ID}."
            )

    @property
    def settings_class(self) -> Optional[Type["BaseSettings"]]:
        """Settings class for the Sagemaker orchestrator.

        Returns:
            The settings class.
        """
        return SagemakerOrchestratorSettings

    def prepare_or_run_pipeline(
        self,
        deployment: "PipelineDeploymentResponseModel",
        stack: "Stack",
    ) -> None:
        """Prepares or runs a pipeline on Sagemaker.

        Args:
            deployment: The deployment to prepare or run.
            stack: The stack to run on.
        """
        if deployment.schedule:
            logger.warning(
                "The Sagemaker Orchestrator currently does not support the "
                "use of schedules. The `schedule` will be ignored "
                "and the pipeline will be run immediately."
            )

        orchestrator_run_name = get_orchestrator_run_name(
            pipeline_name=deployment.pipeline_configuration.name
        ).replace("_", "-")

        session = sagemaker.Session(default_bucket=self.config.bucket)

        sagemaker_steps = []
        for step_name, step in deployment.step_configurations.items():
            image = self.get_image(deployment=deployment, step_name=step_name)
            command = StepEntrypointConfiguration.get_entrypoint_command()
            arguments = StepEntrypointConfiguration.get_entrypoint_arguments(
                step_name=step_name, deployment_id=deployment.id
            )
            entrypoint = command + arguments

            step_settings = cast(
                SagemakerOrchestratorSettings, self.get_settings(step)
            )
            processor_role = (
                step_settings.processor_role or self.config.execution_role
            )

            kwargs = (
                {"tags": [step_settings.processor_tags]}
                if step_settings.processor_tags
                else {}
            )

            processor = sagemaker.processing.Processor(
                role=processor_role,
                image_uri=image,
                instance_count=1,
                sagemaker_session=session,
                instance_type=step_settings.instance_type,
                entrypoint=entrypoint,
                base_job_name=orchestrator_run_name,
                env={
                    ENV_ZENML_SAGEMAKER_RUN_ID: ExecutionVariables.PIPELINE_EXECUTION_ARN,
                },
                volume_size_in_gb=step_settings.volume_size_in_gb,
                max_runtime_in_seconds=step_settings.max_runtime_in_seconds,
                **kwargs,
            )

            sagemaker_step = ProcessingStep(
                name=step.config.name,
                processor=processor,
                depends_on=step.spec.upstream_steps,
            )
            sagemaker_steps.append(sagemaker_step)

        # construct the pipeline from the sagemaker_steps
        pipeline = Pipeline(
            name=orchestrator_run_name,
            steps=sagemaker_steps,
            sagemaker_session=session,
        )

        pipeline.create(role_arn=self.config.execution_role)
        pipeline_execution = pipeline.start()

        # mainly for testing purposes, we wait for the pipeline to finish
        if self.config.synchronous:
            logger.info(
                "Executing synchronously. Waiting for pipeline to finish..."
            )
            pipeline_execution.wait(
                delay=POLLING_DELAY, max_attempts=MAX_POLLING_ATTEMPTS
            )
            logger.info("Pipeline completed successfully.")

    def get_pipeline_run_metadata(
        self, run_id: UUID
    ) -> Dict[str, "MetadataType"]:
        """Get general component-specific metadata for a pipeline run.

        Args:
            run_id: The ID of the pipeline run.

        Returns:
            A dictionary of metadata.
        """
        # TODO: Add this once we can get the region
        # run_url = (
        #     f"https://{region}.console.aws.amazon.com/sagemaker/"
        #     f"home?region={region}"
        # )
        return {
            "pipeline_execution_arn": os.environ[ENV_ZENML_SAGEMAKER_RUN_ID]
        }
