import streamlit as st
import plotly.express as px

st.title("Weather Forecast for the Next Days")
city = st.text_input("City: ")
days = st.slider("Forecast Days", min_value=1,max_value=5,help="Select the number od forecasted days")
option = st.selectbox("Select data to view",("Temperature","Sky"))
st.subheader(f"{option} for the next {days} days in {city}")

def get_data(days):
dates =["2024-12-06","2024-12-07","2024-12-08","2024-12-09"]
temperatures =[20,22,18,17]
temperatures =[days * i for i in temperatures]
return dates,temperatures

d, t = get_data(days)
figure = px.line(x=d,y=t,labels={"x":"Date","y":"Temperature(C)"})
st.plotly_chart(figure)