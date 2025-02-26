from mlflow.tracking import MlflowClient
import mlflow
import pandas as pd
import pickle
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# class InputData(BaseModel):
#     value: float

class RideRequest(BaseModel):
    PULocationID: str
    DOLocationID: str
    trip_distance: float

def load_model():
    mlflow.set_tracking_uri("http://127.0.0.1:5000")
    client = MlflowClient("http://127.0.0.1:5000")
    # print(mlflow.get_tracking_uri()) 

    experiment_id = client.get_experiment_by_name("experiment-1").experiment_id
    runs = client.search_runs(experiment_ids=[experiment_id], order_by=["start_time desc"], max_results=1)
    run_id = runs[0].info.run_id
    # print(run_id)

    # model = mlflow.sklearn.load_model(f"runs:/{run_id}/model")
    model = mlflow.pyfunc.load_model(f"runs:/{run_id}/model")

    artifact_uri = f"runs:/{run_id}/artifacts/dv.pkl"
    dv_path = mlflow.artifacts.download_artifacts(artifact_uri=artifact_uri)
    with open(dv_path, "rb") as f_in:
        dv = pickle.load(f_in)
    print(dv)

    return model, dv

def read_inference_dataframe(path):
    df = pd.read_parquet(path, engine="pyarrow")
    df = df.head(1)
    return df.to_dict(orient="records")[0]

def prepare_features(ride):
    features = {}
    features['PU_DO'] = '%s_%s' % (ride['PULocationID'], ride['DOLocationID'])
    features['trip_distance'] = ride['trip_distance']
    return features

def predict(model, dv, features):
    # features = {'PU_DO': '138_33', 'trip_distance': 9.76}
    features = dv.transform(features)

    preds = model.predict(features)  
    return float(preds[0])

model, dv = load_model()

@app.get("/")
def home():
    return {"message": "FastAPI is running!"}

@app.get("/predict")
def run():
    ride = read_inference_dataframe("../data/yellow_tripdata_2024-12.parquet")
    features = prepare_features(ride)
    prediction = predict(model, dv, features)
    return {"prediction": prediction}