from fastapi import FastAPI
from data_model import TaxiRide, TaxiRidePrediction
from predict import predict
import requests
import json


app = FastAPI()


@app.get('/')
def index():
    return {'message': 'hi hello'}


@app.post('/predict')
def predict_duration(data: TaxiRide):
    prediction = predict('green-taxi-trip-duration-lr-mlops-project', data)
    # Post prediction to evidently:
    data = {
        'PULocationID': data['PULocationID'],
        'DOLocationID': data['DOLocationID'],
        'trip_distance': data['trip_distance'],
        'passenger_count': data['passenger_count'],
        'fare_amount': data['fare_amount'],
        'total_amount': data['total_amount'],
        'prediction': prediction
    }
    json_data = json.dumps(data)
    response = requests.post(
        f'http://localhost:8085/post_prediction',
        data=json_data,
        headers={'content-type': 'application/json'}
    )
    return TaxiRidePrediction(**data.dict(), prediction=prediction)