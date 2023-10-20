import pandas as pd
import tensorflow as tf
import holidays
import joblib
import random

from prophet import Prophet
from sklearn.model_selection import ParameterGrid
from sklearn.metrics import mean_absolute_error
from prophet.serialize import model_to_json, model_from_json
from sklearn.metrics import mean_absolute_percentage_error

try:
    tpu = tf.distribute.cluster_resolver.TPUClusterResolver()  # TPU detection. No parameters necessary if TPU_NAME environment variable is set. On Kaggle this is always the case.
    print('Running on TPU ', tpu.master())
except ValueError:
    tpu = None

if tpu:
    tf.config.experimental_connect_to_cluster(tpu)
    tf.tpu.experimental.initialize_tpu_system(tpu)
    strategy = tf.distribute.experimental.TPUStrategy(tpu)
else:
    strategy = tf.distribute.get_strategy() # default distribution strategy in Tensorflow. Works on CPU and single GPU.


class PowerForcasting():

    def __init__(self, train_data, test_data, model_path):
        self.model_path = model_path
        self.train_data = train_data
        self.test_data = test_data
        holiday = pd.DataFrame()
        for date, name in sorted(
                holidays.UnitedStates(years=[2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019]).items()):
            holiday = pd.concat([holiday, pd.DataFrame([{'ds': date, 'holiday': "US-Holidays"}])], axis=0,
                                ignore_index=True)

        holiday['ds'] = pd.to_datetime(holiday['ds'], format='%Y-%m-%d', errors='ignore')
        self.holiday = holiday
        self.model = self.train_save_final_model()

    def load_model(self):
        final_model = joblib.load(self.model_path)
        return final_model

    def forecasting(self, given_date):
        test_date = {'ds': given_date}
        output = self.model.predict(pd.DataFrame([test_date]))
        self.result = {'date': output.ds, 'power consumsion': output.yhat}
        return self.result

    def get_optimal_value_of_model(self):
        params_grid = {'seasonality_mode': ('multiplicative', 'additive'),
                       'changepoint_prior_scale': [0.1, 0.2, 0.3, 0.4, 0.5],
                       'holidays_prior_scale': [0.1, 0.2, 0.3, 0.4, 0.5],
                       'n_changepoints': [100, 150, 200]}
        grid = ParameterGrid(params_grid)
        cnt = 0
        for p in grid:
            cnt = cnt + 1

        print('Total Possible Models', cnt)
        model_parameters = pd.DataFrame(columns=['MAE', 'Parameters'])
        with strategy.scope():
            for p in grid:
                test = pd.DataFrame()
                print(p)
                random.seed(0)
                train_model = Prophet(changepoint_prior_scale=p['changepoint_prior_scale'],
                                      holidays_prior_scale=p['holidays_prior_scale'],
                                      n_changepoints=p['n_changepoints'],
                                      seasonality_mode=p['seasonality_mode'],
                                      weekly_seasonality=True,
                                      daily_seasonality=True,
                                      yearly_seasonality=True,
                                      holidays=self.holiday,
                                      interval_width=0.95)
                train_model.add_country_holidays(country_name='US')
                train_model.fit(self.train_data)
                test_forecast = train_model.predict(self.test_data)
                y_true = self.test_data['y']
                y_pred = test_forecast['yhat']
                MAPE = mean_absolute_percentage_error(y_true, y_pred)
                print('Mean Absolute Percent Error(MAPE)------------------------------------', MAPE)
                model_parameters = pd.concat([model_parameters, pd.DataFrame([{'MAPE': MAPE, 'Parameters': p}])],
                                             axis=0,
                                             ignore_index=True)
            best_parameters = model_parameters.iloc[model_parameters.MAPE.argmin()].Parameters
        return best_parameters

    def train_save_final_model(self):
        best_parameters = self.get_optimal_value_of_model()
        final_model = Prophet(holidays=self.holiday,
                              changepoint_prior_scale=best_parameters.get('changepoint_prior_scale'),
                              holidays_prior_scale=best_parameters.get('holidays_prior_scale'),
                              n_changepoints=best_parameters.get('n_changepoints'),
                              seasonality_mode=best_parameters.get('seasonality_mode'),
                              weekly_seasonality=False,
                              daily_seasonality=False,
                              yearly_seasonality=True,
                              interval_width=0.95)
        final_model.add_country_holidays(country_name='US')
        final_model.fit(self.train_data)
        self.model = final_model
        with open(self.model_path, 'w') as f:
            f.write(model_to_json(self.model))





class PowerConsumsionForecasting():

    def __init__(self,model_path='model.json'):
        with open(model_path, 'r') as f:

            self.model = model_from_json(f.read())

    def predict(self, given_date):
        test_date = {'ds': given_date}
        output = self.model.predict(pd.DataFrame([test_date]))
        result = {"date": output.iloc[0].ds, "power forcasting": output.iloc[0].yhat}
        return result




