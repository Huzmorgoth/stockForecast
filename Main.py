import streamlit as st
import datetime
import pandas as pd
import pandas_datareader as pdr
from tensorflow.keras.models import model_from_yaml
from performForecastClassFile import performForecast
import altair as alt

yaml_file = open('model/rel_model.yaml', 'r')
loaded_model_yaml = yaml_file.read()
yaml_file.close()
lstm = model_from_yaml(loaded_model_yaml)
# load weights into new model
lstm.load_weights("model/rel_model.h5")
print("Loaded model from disk")  # Load "model"
print('Model loaded')

st.subheader('Reliance Stock Forecast')

df = pdr.DataReader('RELIANCE.BO', 'yahoo')
df = df.reset_index()

cs_slide = st.slider('Number of Days', 1, df.shape[0]+1, 30)

base = alt.Chart(df.tail(cs_slide)).encode(
    alt.X('Date:T', axis=alt.Axis(labelAngle=-45)),
    color=alt.condition("datum.Open <= datum.Close",
                        alt.value("#06982d"), alt.value("#ae1325"))
)

chart = alt.layer(
    base.mark_rule().encode(alt.Y('Low:Q', title='Price',
                                    scale=alt.Scale(zero=False)), alt.Y2('High:Q')),
    base.mark_bar().encode(alt.Y('Open:Q'), alt.Y2('Close:Q')),
).interactive()

st.altair_chart(chart, use_container_width=True)


def load_data(user_input):
    prediction = performForecast(int(user_input)).predict(lstm)
    base = datetime.datetime.today()
    date_list = [(base + datetime.timedelta(days=x + 1)).strftime('%m-%d-%Y') for x in range(int(user_input))]
    df = pd.DataFrame()
    df['Date'] = date_list
    df['Date'] = pd.to_datetime(df['Date'])
    df['Future_prices'] = [abs(pred) for pred in prediction]
    return df


default = 10
future_days = st.slider('Number of Future Forecast Days', 1, 30, default)
data = load_data(future_days)

if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(data)

st.subheader('Stock closing on each day')
st.line_chart(data['Future_prices'])
