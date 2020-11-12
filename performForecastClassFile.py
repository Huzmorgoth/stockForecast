"""Importing relevant packages"""
import pandas_datareader as web
import numpy as np
from sklearn.preprocessing import MinMaxScaler

"""----CLASS DEFINITION-----"""

class performForecast:
    def __init__(self, fDays):
        self.UserInput = fDays
        self.df = web.DataReader('RELIANCE.BO', 'yahoo')
        self.df.reset_index(inplace=True)
        self.df['ser'] = [x for x in range(self.df.shape[0])]
        self.time_steps = 10
        self.df_stock = self.df[['ser', 'Close']].tail(10)

    def scaleDS(self, Input, f_transformer, t_transformer, Features):
        f_transformer = f_transformer.fit(Input[Features].to_numpy())
        t_transformer = t_transformer.fit(Input[['Close']].to_numpy())

        Input.loc[:, Features] = f_transformer.transform(Input[Features].to_numpy())
        Input['Close'] = t_transformer.transform(Input[['Close']].to_numpy())

        return Input

    def create_dataset(self, X, time_steps=1):
        Xs = []
        v = X.iloc[0:time_steps].values
        Xs.append(v)
        return np.array(Xs)

    def predict(self, loaded_model):
        f_transformer = MinMaxScaler()  # Feature scaler
        t_transformer = MinMaxScaler()
        df_out = []

        for x in range(self.UserInput):
            self.df_stock = self.df_stock.tail(self.time_steps)
            Input = self.df_stock.copy()
            Features = Input.columns
            X_input_lstm = self.create_dataset(self.scaleDS(Input, f_transformer, t_transformer, Features),
                                               self.time_steps)
            y_pred = loaded_model.predict(X_input_lstm)
            y_pred_inv = t_transformer.inverse_transform(y_pred)
            inClose = y_pred_inv[0][0]
            inSer = int(self.df_stock.ser.tail(1))
            self.df_stock = self.df_stock.append({'ser': inSer + 1, 'Close': y_pred_inv[0][0]}, ignore_index=True)
            df_out.append(y_pred_inv[0][0])

        return df_out

"""----CLASS DEFINITION-----"""