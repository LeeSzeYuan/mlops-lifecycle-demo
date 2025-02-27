from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Define a request model
class InputData(BaseModel):
    value: float

@app.get("/")
def home():
    return {"message": "FastAPI is running!"}

@app.post("/predict")
def predict(data: InputData):
    prediction = data.value * 2  # Dummy logic for testing
    return {"prediction": prediction}

