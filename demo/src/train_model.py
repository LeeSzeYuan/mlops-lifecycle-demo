from sklearn.feature_extraction import DictVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.linear_model import Lasso
import mlflow.sklearn
import pandas as pd
import pickle
import mlflow
import sys 

def train_model_and_log_mlflow(path):
    df = pd.read_parquet(path, engine="pyarrow")
    
    categorical = ['PU_DO']
    numerical = ['trip_distance']
    target = 'duration'

    x_train, x_val, y_train, y_val = train_test_split(df, df[target], test_size=0.2, random_state=40)

    dv = DictVectorizer()
    X_train = dv.fit_transform(x_train[categorical + numerical].to_dict(orient='records'))
    X_val = dv.transform(x_val[categorical + numerical].to_dict(orient='records'))

    alpha = 0.1
    lr = Lasso(alpha)
    lr.fit(X_train, y_train)

    y_pred = lr.predict(X_val)
    rmse = mean_squared_error(y_val, y_pred)

    print(f"Validation RMSE: {rmse:.4f}")

    with open("models/dv.pkl", "wb") as f_out:
        pickle.dump(dv, f_out)

    # with open("../models/model.pkl", "wb") as f_out:
    #     pickle.dump(lr, f_out)
        
    mlflow.set_tracking_uri("http://127.0.0.1:5000")
    mlflow.set_experiment("experiment-1")
    with mlflow.start_run():
        mlflow.log_param("alpha", alpha)
        mlflow.log_metric("rmse", rmse)
        mlflow.sklearn.log_model(lr, artifact_path="model")
        mlflow.log_artifact("models/dv.pkl", artifact_path="artifacts")
        
    return rmse

if __name__ == "__main__":
    path = sys.argv[1]  # Read input file path from command-line args
    df = train_model_and_log_mlflow(path)