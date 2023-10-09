from . import db


class Predictions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    PULocationID = db.Column(db.Integer)
    DOLocationID = db.Column(db.Integer)
    trip_distance = db.Column(db.Float)
    passenger_count = db.Column(db.Float)
    fare_amount = db.Column(db.Float)
    total_amount = db.Column(db.Float)
    prediction = db.Column(db.Float)


class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime)
    prediction_drift = db.Column(db.Float)
    num_drifted_columns = db.Column(db.Integer)
    share_missing_values = db.Column(db.Float)