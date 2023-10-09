import os
import pandas as pd
import mlflow
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_absolute_percentage_error
from sklearn.linear_model import LinearRegression



GOOGLE_APPLICATION_CREDENTIALS = './credentials.json'
# GOOGLE_APPLICATION_CREDENTIALS = '../service-account-key.json'
MLFLOW_TRACKING_URI = os.getenv('MLFLOW_TRACKING_URI')
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = GOOGLE_APPLICATION_CREDENTIALS


mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
mlflow.set_experiment('green-taxi-mlops-project')


color = 'green'
year = 2021
month = 1
features = ['PULocationID', 'DOLocationID', 'trip_distance', 'passenger_count', 'fare_amount', 'total_amount']
target = 'duration'
model_name = 'green-taxi-trip-duration-lr-mlops-project'


def load_new_training_data(color, year, month):
    if not os.path.exists(f'./data/{color}_tripdata_{year}-{month:02d}.parquet'):
        os.system(f'wget -P ./data https://d37ci6vzurychx.cloudfront.net/trip-data/{color}_tripdata_{year}-{month:02d}.parquet')
    df = pd.read_parquet(f'./data/{color}_tripdata_{year}-{month:02d}.parquet')
    return df


def calculate_trip_duration_in_minutes(df):
    df['duration'] = (df['lpep_dropoff_datetime'] - df['lpep_pickup_datetime']).dt.total_seconds() / 60
    df = df[(df['duration'] >= 1) & (df['duration'] <= 60)]
    df = df[(df['passenger_count'] > 0) & (df['passenger_count'] < 8)]
    df = df[features + [target]]
    return df


def save_reference_data(X_train, y_train):
    y_pred_train = lr.predict(X_train)
    reference_data = X_train.copy()
    reference_data['duration'] = y_train
    reference_data['prediction'] = y_pred_train
    reference_data.to_parquet('gs://mlops-final-project/reference_data/reference_data.parquet')


df = load_new_training_data(color, year, month)

df_processed = calculate_trip_duration_in_minutes(df)

y = df_processed['duration']
X = df_processed.drop(columns=['duration'])

X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42, test_size=0.2)


with mlflow.start_run() as run:
    tags = {
        'model': 'linear regression',
        'developer': 'karim',
        'dataset': 'green-taxi',
        'year': year,
        'month': month,
        'features': features,
        'target': target
    }
    mlflow.set_tags(tags)

    lr = LinearRegression()
    lr.fit(X_train, y_train)

    save_reference_data(X_train, y_train)

    y_pred = lr.predict(X_test)
    rmse = mean_squared_error(y_test, y_pred, squared=False)
    mlflow.log_metric('rmse', rmse)

    mlflow.sklearn.log_model(lr, 'model')
    run_id = mlflow.active_run().info.run_id

    model_uri = f'runs:/{run_id}/model'
    mlflow.register_model(model_uri=model_uri, name=model_name)

    model_version = 1
    new_stage = 'Production'
    client.transition_model_version_stage(
        name=model_name,
        version=model_version,
        stage=new_stage,
        archive_existing_versions=False
    )