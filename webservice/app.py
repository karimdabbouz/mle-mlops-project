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
    prediction_data = {
        'PULocationID': data.PULocationID,
        'DOLocationID': data.DOLocationID,
        'trip_distance': data.trip_distance,
        'passenger_count': data.passenger_count,
        'fare_amount': data.fare_amount,
        'total_amount': data.total_amount,
        'prediction': prediction
    }
    print(prediction_data)
    json_data = json.dumps(prediction_data)
    try:
        response = requests.post(
            'http://10.156.0.6:8085/post_prediction',
            data=json_data,
            headers={'content-type': 'application/json'}
        )
        print(response)
        print(response.text)
    except requests.exceptions.ConnectionError as error:
        print(f"Cannot reach a metrics application, error: {error}, data: {data}")
    return TaxiRidePrediction(**data.dict(), prediction=prediction)