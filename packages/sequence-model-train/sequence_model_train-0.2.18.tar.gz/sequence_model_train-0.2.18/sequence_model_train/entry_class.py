from .data.data_pipeline import get_dataloader, get_uniq_data
from .utils.train_nn import TrainNNModel
from .models.arima_model import ArimaModel


class Offline:
    def __init__(self):
        self.model = None
        self.model_type = None
        self.support_models = {
            'nn': ['lstm', 'tcn'],
            'arma': ['arima'],
            'tbase': ['xgb']
        }
        self.data_prams = {
            'train_data_path': None,
            'train_start_date': '2021-01-01',
            'train_end_date': '2023-01-01',
            'valid_start_date': '2023-01-01',
            'valid_end_date': '2023-03-01'
        }
        self.model_params = {
            'n_in': 30,
            'n_out': 7,
            'batch_size': 32,
            'hidden_size': 32,
            'num_layers': 3,
            'input_size': 10
        }
        self.result = None

    def update_params(self, **kwargs):
        self.model = kwargs.get('model', self.model)
        self.model_type = kwargs.get('model_type', self.model_type)
        self.model_params['n_in'] = kwargs.get(
            'n_in',
            self.model_params['n_in']
        )
        self.model_params['n_out'] = kwargs.get(
            'n_out',
            self.model_params['n_out']
        )
        self.model_params['batch_size'] = kwargs.get(
            'batch_size',
            self.model_params['batch_size']
        )
        self.model_params['hidden_size'] = kwargs.get(
            'hidden_size',
            self.model_params['hidden_size']
        )
        self.model_params['num_layers'] = kwargs.get(
            'num_layers',
            self.model_params['num_layers']
        )
        self.data_prams['train_data_path'] = kwargs.get(
            'train_data_path',
            self.data_prams['train_data_path']
        )
        self.data_prams['train_start_date'] = kwargs.get(
            'train_start_date',
            self.data_prams['train_start_date']
        )
        self.data_prams['train_end_date'] = kwargs.get(
            'train_end_date',
            self.data_prams['train_end_date']
        )
        self.data_prams['valid_start_date'] = kwargs.get(
            'valid_start_date',
            self.data_prams['valid_start_date']
        )
        self.data_prams['valid_end_date'] = kwargs.get(
            'valid_end_date',
            self.data_prams['valid_end_date']
        )

    def train_model(self):
        if self.model_type in self.support_models['nn']:
            t_, v_, n_ = get_dataloader(self.train_data_path,
                                        self.model_params['n_in'],
                                        self.model_params['n_out'],
                                        self.data_prams['train_start_date'],
                                        self.data_prams['train_end_date'],
                                        self.data_prams['valid_start_date'],
                                        self.data_prams['valid_end_date'],
                                        self.model_params['batch_size'])
            params = {
                'input_size': n_,
                'hidden_size':  self.model_params['hidden_size'],
                'num_layers': self.model_params['num_layers'],
                'output_size': self.model_params['n_out'],
            }
            model = TrainNNModel(params, self.model_type)
        if self.model_type in self.support_models['arma']:
            t_, v_ = get_uniq_data(self.train_data_path,
                                   self.model_params['n_out'])
            model = ArimaModel(self.model_params['n_out'])
        self.model = model.fit(t_, v_)
        self.result = self.model.get_base_line()
        return self.result
