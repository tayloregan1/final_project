import streamlit as st
import pandas as pd
import plotly.express as px

st.write('Hello')
shark = pd.read_csv('cleaned_sharks.csv')

unprov = len(shark[shark['Type'] == 'Unprovoked'])/len(shark)
prov = len(shark[shark['Type'] == 'Provoked'])/len(shark)
null = len(shark[shark['Type'].isnull()])/len(shark)
type_dictionary = {'Provoked': prov, 'Unprovoked': unprov, 'Other':null}

types = type_dictionary.keys()
freq = type_dictionary.values()
pie_chart = px.pie(values=freq, names=types, color=types, title='Percent of Shark Attacks by Type of Attack')
st.plotly_chart(pie_chart)
