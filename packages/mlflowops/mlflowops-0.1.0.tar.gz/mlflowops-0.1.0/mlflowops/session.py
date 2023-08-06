import os
import re
from typing import Optional

import mlflow
from azure.identity import (
    AzureCliCredential,
    ChainedTokenCredential,
    ClientSecretCredential,
    DefaultAzureCredential,
    InteractiveBrowserCredential,
    ManagedIdentityCredential,
    VisualStudioCodeCredential,
)
from pydantic import BaseSettings, validator


class MLFlowSession(BaseSettings):
    deployment_client: Optional[object] = None

    class Config:
        env_file = ".env"

    def get_deployment_client(self, client_name: str):
        from mlflow.deployments import get_deploy_client

        self.deployment_client = get_deploy_client(client_name)
        return self.deployment_client


class DatabricksMLFlowSession(MLFlowSession):
    databricks_experiment_name: str = "mlflow_experiments"
    databricks_experiment_id: Optional[str] = None
    databricks_username: Optional[str] = None
    databricks_token: Optional[str] = None
    databricks_host: Optional[str] = None
    databricks_password: Optional[str] = databricks_token
    _mlflow_tracking_uri: Optional[str] = "databricks"

    @validator("databricks_host", pre=True, always=True)
    def check_https_pattern(cls, path):
        if not re.match(r"^https://", path):
            path = f"https://{path}"
        return path

    def get_session(self):
        print("Creating a Databricks MLFlow Session")
        os.environ["experiment_id"] = self.databricks_experiment_id
        # Set the Databricks credentials
        os.environ["DATABRICKS_HOST"] = self.databricks_host
        os.environ["DATABRICKS_TOKEN"] = self.databricks_token
        os.environ["MLFLOW_TRACKING_URI"] = self._mlflow_tracking_uri
        os.environ["DATABRICKS_USERNAME"] = self.databricks_username
        os.environ["DATABRICKS_PASSWORD"] = self.databricks_password

        # Set the tracking uri
        mlflow.set_tracking_uri(self._mlflow_tracking_uri)
        mlflow.set_experiment(self.databricks_experiment_name)

        return mlflow


class AzureMLFlowSession(MLFlowSession):
    azureml_experiment_name: str = "tse_prophet_hyperopt"
    azureml_experiment_id: Optional[str] = None
    azureml_subscription_id: Optional[str] = None
    azureml_resource_group: Optional[str] = None
    azureml_workspace_name: Optional[str] = None
    azureml_credential: Optional[object] = None

    def init_credential(
        self,
        credential_type: str = "DefaultAzureCredential",
        credential_args: dict = None,
    ):
        if credential_args is None:
            credential_args = {}
        # Map string names to azure.identity classes
        credential_types = {
            "DefaultAzureCredential": DefaultAzureCredential,
            "ClientSecretCredential": ClientSecretCredential,
            "ChainedTokenCredential": ChainedTokenCredential,
            "ManagedIdentityCredential": ManagedIdentityCredential,
            "InteractiveBrowserCredential": InteractiveBrowserCredential,
            "VisualStudioCodeCredential": VisualStudioCodeCredential,
            "AzureCliCredential": AzureCliCredential,
            # add more classes here as needed
        }

        # Check if the credential is already defined, if not, create a new one of the specified type
        if self.azureml_credential is None:
            if credential_type in credential_types:
                self.azureml_credential = credential_types[credential_type](
                    **credential_args
                )
            else:
                raise ValueError(f"Invalid credential type: {credential_type}")

    def set_experiment_id(self):
        import os

        os.environ["experiment_id"] = self.azureml_experiment_id

    def get_mlclient(self):
        from azure.ai.ml import MLClient

        ml_client = MLClient(
            credential=self.azureml_credential,
            subscription_id=self.azureml_subscription_id,
            resource_group_name=self.azureml_resource_group,
            workspace_name=self.azureml_workspace_name,
        )
        return ml_client

    def setup_mlflow(self, ml_client):
        mlflow_tracking_uri = ml_client.workspaces.get(
            ml_client.workspace_name
        ).mlflow_tracking_uri
        mlflow.set_tracking_uri(mlflow_tracking_uri)
        mlflow.set_experiment(self.azureml_experiment_name)

    def get_session(
        self,
        credential_type: str = "DefaultAzureCredential",
        credential_args: dict = None,
    ):
        if credential_args is None:
            credential_args = {}
        self.init_credential(credential_type, credential_args)
        self.set_experiment_id()
        ml_client = self.get_mlclient()
        self.setup_mlflow(ml_client)
        return ml_client
