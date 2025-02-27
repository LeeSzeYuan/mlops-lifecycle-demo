import mlflow
from mlflow.tracking import MlflowClient

def register_model():
    client = MlflowClient("http://127.0.0.1:5000")
    experiment_id = client.get_experiment_by_name("experiment-1").experiment_id
    runs = client.search_runs(experiment_ids=[experiment_id], order_by=["start_time desc"], max_results=1)
    run_id = runs[0].info.run_id
    # print(run_id)

    # Register model in Registry
    mlflow.register_model(
        model_uri=f"runs:/{run_id}/models",
        name='nyc-taxi-regression-model-tracking-server'
    )
