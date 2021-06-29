# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import streamlit as st
import pandas as pd
from openpyxl import load_workbook
import matplotlib.pyplot as plt
# %%
st.write('Hello')
shark = pd.read_csv('cleaned_sharks.csv')
# %%
unprov = len(shark[shark['Type'] == 'Unprovoked'])/len(shark)
prov = len(shark[shark['Type'] == 'Provoked'])/len(shark)
null = len(shark[ shark['Type'].isnull() ])/len(shark)
type_dictionary = {'Provoked':prov, 'Unprovoked':unprov, 'Other':null}

labels = type_dictionary.keys()
sizes = type_dictionary.values()
# explode = (0, 0.1, 0, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')

fig1, ax1 = plt.subplots()
ax1.pie(sizes, labels=labels, autopct='%1.1f%%',
        shadow=True, startangle=90)
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

st.pyplot(plt.gcf())


# %%

# %%
