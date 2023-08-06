from ..utils.model_process import caculate_eval
from ngboost import NGBRegressor


class NGBoostModel:
    def __init__(self, columns, n_in, n_out):
        self.columns = columns
        self.n_in = n_in
        self.n_out = n_out
        self.models = []
        self.result = {}

    def fit(self, X, y):
        self.models = []
        columns_ = X.columns.difference(self.columns)
        columns_ = X[columns_].select_dtypes(include=['float']).columns.values
        self.columns = X[self.columns].select_dtypes(
            include=['float']
        ).columns.values
        print(self.columns)
        for i in range(self.n_out):
            ngb = NGBRegressor(
                n_estimators=100,
                learning_rate=0.01,
                verbose=False
            )
            ngb.fit(X[columns_].values, X[self.columns].values[:, i])
            self.models.append(ngb)
        pred_y = []
        for i in range(self.n_out):
            if (i+1-self.n_out == 0):
                pred_y.append(
                    self.models[i].predict(y.values[-1:, :])[0]
                )
            else:
                pred_y.append(
                    self.models[i].predict(
                        y.values[i-self.n_out:i+1-self.n_out, :]
                    )[0]
                )
        print(pred_y)
        print(y.values[0:1, :])
        mse, mae, mape = caculate_eval(pred_y, y.values[-1:, :][0])
        self.result = dict(
            model='ngboost',
            valid_result=dict(
                valid_loss=mse,
                valid_mae=mae,
                valid_mape=mape
            ),
            train_process=dict()
        )
        return self.models

    def get_base_line(self):
        return self.result
