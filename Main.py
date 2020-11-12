import streamlit as st
import datetime
import pandas as pd
from tensorflow.keras.models import model_from_yaml
from performForecastClassFile import performForecast


yaml_file = open('model/rel_model.yaml', 'r')
loaded_model_yaml = yaml_file.read()
yaml_file.close()
lstm = model_from_yaml(loaded_model_yaml)
# load weights into new model
lstm.load_weights("model/rel_model.h5")
print("Loaded model from disk") # Load "model"
print('Model loaded')

st.subheader('Reliance Stock Forecast')
#@st.cache
def load_data(user_input):
    prediction = performForecast(int(user_input)).predict(lstm)
    base = datetime.datetime.today()
    date_list = [(base + datetime.timedelta(days=x + 1)).strftime('%m-%d-%Y') for x in range(int(user_input))]
    DF = pd.DataFrame()
    DF['Date'] = date_list
    DF['Date'] = pd.to_datetime(DF['Date'])
    DF['Future_prices'] = prediction
    return DF

default = 10
future_days = st.slider('Number of Future Forecast Days', 1, 30, default)
data = load_data(future_days)

if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(data)

st.subheader('Stock closing on each day')
st.line_chart(data['Future_prices'])

