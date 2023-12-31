from .models import Predictions, SessionLocal
from evidently.report import Report
from evidently import ColumnMapping
from evidently.metrics import (
    ColumnDriftMetric,
    DatasetDriftMetric,
    DatasetMissingValuesMetric,
)



def load_last_50_predictions():
    db = SessionLocal()
    last_50_rows = db.query(Predictions).order_by(Predictions.id.desc()).limit(50).all()
    db.close()
    return last_50_rows


def create_report(reference_data, df, num_features, cat_features):
    column_mapping = ColumnMapping(
        prediction='prediction',
        numerical_features=num_features,
        categorical_features=cat_features
    )
    report = Report(
        metrics=[
            ColumnDriftMetric(column_name='prediction'),
            DatasetDriftMetric(),
            DatasetMissingValuesMetric(),
        ]
    )
    report.run(
        reference_data=reference_data, current_data=df, column_mapping=column_mapping
    )
    result = report.as_dict()
    return result