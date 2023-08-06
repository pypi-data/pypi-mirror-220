import math

import mlflow
from mlflow.tracking import MlflowClient


class MLFlowOps:
    def __init__(
        self,
        runs_names: list,
        base_model_name: str,
        experiment_ids: str = None,
        sorting_metric: str = "metrics.val_rmse",
        ascending: bool = True,
    ):
        self.runs_names = runs_names
        self.base_model_name = base_model_name
        self.experiment_ids = experiment_ids.split(",")
        self.sorting_metric = sorting_metric
        self.ascending = ascending

    def get_best_run_model(self, run_name: str):
        mlflow_runs = mlflow.search_runs(
            experiment_ids=self.experiment_ids, filter_string=f"run_name='{run_name}'"
        )
        sorted_runs = mlflow_runs.sort_values(
            by=[self.sorting_metric], ascending=self.ascending
        )
        return sorted_runs.iloc[0]

    def get_most_recent_run_model(self, run_name: str):
        mlflow_runs = mlflow.search_runs(
            experiment_ids=self.experiment_ids, filter_string=f"run_name='{run_name}'"
        )
        sorted_runs = mlflow_runs.sort_values(by=["end_time"], ascending=False)
        return sorted_runs.iloc[0]

    def register_best_model(self, run_id, model_name):
        model_path = f"runs:/{run_id}/model"
        # loaded_model = mlflow.pyfunc.load_model(model_path)
        return mlflow.register_model(model_path, model_name)

    def transition_model(self, model_name, model_version, stage="Production"):
        client = MlflowClient()
        version = int(model_version.version)
        registered_version = client.transition_model_version_stage(
            name=model_name,
            version=version,
            stage=stage,
        )
        if version != 0:
            try:
                client.transition_model_version_stage(
                    name=model_name,
                    version=version - 1,
                    stage="Archived",
                )
            except:
                pass
        return registered_version

    def check_model_improvement_and_transition_in_training_loop(
        self, training_loss, training_run_id, stage="Production"
    ):
        run_name = self.runs_names[0]
        model_name = f"{self.base_model_name}_{run_name}"
        if self.has_improved(run_name=run_name, most_recent_loss=training_loss):
            model_version = self.register_best_model(
                run_id=training_run_id, model_name=model_name
            )
            transitioned_model = self.transition_model(model_name, model_version, stage)
            return transitioned_model

    def register_and_transition_models(self, stage="Production"):
        for run_name in self.runs_names:
            model_name = f"{self.base_model_name}_{run_name}"
            most_recent_run = self.get_most_recent_run_model(
                run_name
            )  # self.get_best_run_model(run_name)['run_id']
            if self.has_improved(
                run_name=run_name, most_recent_loss=most_recent_run[self.sorting_metric]
            ):
                model_version = self.register_best_model(
                    run_id=most_recent_run["run_id"], model_name=model_name
                )
                transitioned_model = self.transition_model(
                    model_name, model_version, stage
                )
                return transitioned_model

    def get_registered_models(
        self,
    ):
        return mlflow.tracking.MlflowClient().search_registered_models(max_results=1000)

    def get_registered_model(self, model_name):
        return mlflow.tracking.MlflowClient().get_registered_model(model_name)

    def list_registered_models(self):
        return [
            (model.name, model.latest_versions)
            for model in self.get_registered_models()
        ]

    def delete_experiment_runs(self, state="FAILED"):
        # Get a list of all runs in the experiment
        runs = mlflow.search_runs(
            self.experiment_ids, filter_string=f"status='{state}'"
        )
        # Loop through the runs and delete any that have a status of "FAILED"
        for _, row in runs.iterrows():
            print(f"Deleting run with ID: {row['run_id']}")
            mlflow.delete_run(row["run_id"])

    def transition_all_to_none(self):
        for model in self.get_registered_models():
            # if model.latest_versions:
            for version in model.latest_versions:
                if version.current_stage in ["Staging", "Production"]:
                    mlflow.tracking.MlflowClient().transition_model_version_stage(
                        name=model.name, version=version.version, stage="None"
                    )

    def purge_registered_models(self):
        while len(self.get_registered_models()) > 0:
            for model in self.get_registered_models():
                for version in model.latest_versions:
                    if version.current_stage in ["Staging", "Production"]:
                        print(
                            f"Transitioning {model.name} and version {version.version} to None"
                        )
                        mlflow.tracking.MlflowClient().transition_model_version_stage(
                            name=model.name, version=version.version, stage="None"
                        )
                print(f"Deleting {model.name}")
                mlflow.tracking.MlflowClient().delete_registered_model(model.name)

    def delete_registered_none_models(self):
        for model in self.get_registered_models():
            mlflow.tracking.MlflowClient().delete_registered_model(model.name)

    def get_registered_model_metrics(self, run_name, stage="Production"):
        try:
            model_uri = f"models:/{self.base_model_name}_{run_name}/{stage}"
            model = mlflow.pyfunc.load_model(model_uri)
            metrics = mlflow.get_run(model.metadata.run_id).data.metrics
            return {f"metrics.{k}": v for k, v in metrics.items()}[self.sorting_metric]
        except Exception as e:
            print(e)
            return math.inf

    def get_registered_model_function(self, run_name, stage="Production"):
        try:
            model_uri = f"models:/{self.base_model_name}_{run_name}/{stage}"
            return mlflow.pyfunc.load_model(model_uri)
        except Exception as e:
            print(e)
            return None

    def has_improved(self, run_name, most_recent_loss) -> bool:
        registered_model_loss = self.get_registered_model_metrics(run_name)
        return most_recent_loss < registered_model_loss


def init():
    print("MLFlowOps Utility Installed")
