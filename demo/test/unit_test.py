from mlflow.tracking import MlflowClient
import mlflow
import pickle
from src.serving import load_model, predict

# helper function
def get_run_id():
    mlflow.set_tracking_uri("http://127.0.0.1:5000")
    client = MlflowClient("http://127.0.0.1:5000")

    experiment_id = client.get_experiment_by_name("experiment-1").experiment_id
    runs = client.search_runs(experiment_ids=[experiment_id], order_by=["start_time desc"], max_results=1)
    run_id = runs[0].info.run_id

    return run_id

# unit test if model can be loaded
def test_load_model():
    run_id = get_run_id()

    model = mlflow.pyfunc.load_model(f"runs:/{run_id}/model")

    assert model is not None

# unit test if load dictVectorizer can be loaded
def test_load_dv():
    run_id = get_run_id()

    artifact_uri = f"runs:/{run_id}/artifacts/dv.pkl"
    dv_path = mlflow.artifacts.download_artifacts(artifact_uri=artifact_uri)
    with open(dv_path, "rb") as f_in:
        dv = pickle.load(f_in)

    assert dv is not None

# unit test if prediction function usable for FastAPI app
def test_predict():
    model, dv = load_model()
    features = {'PU_DO': '138_33', 'trip_distance': 9.76}
    prediction = predict(model, dv, features)
    assert prediction > 0