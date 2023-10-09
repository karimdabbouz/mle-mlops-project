from flask import current_app as app
from flask import request
from werkzeug.middleware.dispatcher import DispatcherMiddleware
import prometheus_client
from . import db
from .utils import create_report, load_last_50_predictions
from .models import Predictions, Report
from sqlalchemy.orm import sessionmaker
import pandas as pd
import datetime



@app.route('/')
def index():
    return 'hi there'


@app.route('/post_prediction', methods=['POST'])
def post_prediction():
    cat_features = ['PULocationID', 'DOLocationID']
    num_features = ['trip_distance', 'passenger_count', 'fare_amount', 'total_amount']
    # this needs to be a gcs path to load the latest reference data generated in the last training run:
    reference_data = pd.read_parquet('./data/reference_data.parquet')
    prediction = request.json
    new_entry = Predictions(**prediction)
    db.session.add(new_entry)
    db.session.commit()
    last_predictions = load_last_50_predictions()
    if len(last_predictions) >= 50:
        df = pd.DataFrame([row.__dict__ for row in last_predictions])
        df = df.drop('_sa_instance_state', axis=1)
        report = create_report(reference_data, df, num_features, cat_features)
        report_dict = {
            'timestamp': datetime.datetime.now(),
            'prediction_drift': report['metrics'][0]['result']['drift_score'],
            'num_drifted_columns': report['metrics'][1]['result'][
                'number_of_drifted_columns'
            ],
            'share_missing_values': report['metrics'][2]['result']['current'][
                'share_of_missing_values'
            ],
        }
        report_entry = Report(**report_dict)
        db.session.add(report_entry)
        db.session.commit()
    return 'prediction and evidently data drift report stored in database'