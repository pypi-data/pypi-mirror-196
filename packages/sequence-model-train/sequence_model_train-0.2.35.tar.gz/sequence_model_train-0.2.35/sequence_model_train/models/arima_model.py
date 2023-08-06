from sklearn.metrics import mean_squared_error, mean_absolute_error, mean_absolute_percentage_error
from statsmodels.tsa.arima.model import ARIMA


class ARIMAModel:
    def __init__(self, output_size):
        self.n_out = output_size
        self.model = None
        self.label_set = None

    def fit(self, X, y):
        airma_model = ARIMA(X.values[:, -1], order=(2, 1, 1))
        airma_fit = airma_model.fit()
        self.model = airma_fit
        self.label_set = y.values[:, -1]
        return self.model

    def predict(self, steps):
        pred_y = self.model.forecast(steps)
        return pred_y

    def get_base_line(self):
        pred_y = self.predict(self.n_out)
        mse = mean_squared_error(self.label_set - pred_y)
        mae = mean_absolute_error(self.label_set, pred_y)
        mape = mean_absolute_percentage_error(self.label_set, pred_y)
        return dict(
            model='arima',
            valid_result=dict(
                valid_loss=mse,
                valid_mae=mae,
                valid_mape=mape
            ),
            train_process=dict()
        )
