import streamlit as st
import pandas as pd
import plotly.express as px


@st.cache
def load_data(filename):
    return pd.read_csv(filename)


shark = load_data('cleaned_sharks.csv')
sharkattack_counts = load_data('sharkattack_counts.csv')

# sidebar
st.sidebar.title('Filter Data Here:')

min_year, max_year = st.sidebar.slider('Years to include:', 1961, 2020, (2000, 2020), 1)
min_age, max_age = st.sidebar.slider('Ages to include:', 3, 87, (18, 35), 1)
countries = st.sidebar.multiselect('Areas to include:', sorted(shark['Country'].unique()))
sex = st.sidebar.multiselect('Sexes to include:', ['M', 'F'])
fatal = st.sidebar.multiselect('Fatality type to include:', [True, False])

st.header('Exploring Shark Attack Data')

# years = range(min_year, max_year + 1)
# ages = range(min_age, max_age + 1)

countries_list = list(countries)
st.write(countries_list)

filtered_df = shark.loc[(shark['Year'] <= max_year) & (shark['Year'] >= min_year)
                        & (shark['Age'] <= max_age) & (shark['Age'] >= min_age)]
filter_countries = filtered_df['Country'].isin(countries_list)
filtered_df = filtered_df[filter_countries]

st.dataframe(filtered_df)

st.header('Percent of Shark Attacks by Type of Attack')
unprov = len(shark[shark['Type'] == 'Unprovoked'])/len(shark)
prov = len(shark[shark['Type'] == 'Provoked'])/len(shark)
null = len(shark[shark['Type'].isnull()])/len(shark)
type_dictionary = {'Provoked': prov, 'Unprovoked': unprov, 'Other':null}
types = type_dictionary.keys()
freq = type_dictionary.values()
pie_chart = px.pie(values=freq, names=types, color=types, title='Pie Chart: Type of Attack')
st.plotly_chart(pie_chart)

# add labels to this graph
st.header("Amount of Shark Attacks per Year")
barplot = pd.pivot_table(sharkattack_counts, index=['Year'], values=['Amount of Shark Attacks'])
barplot.plot(kind='bar')
st.bar_chart(barplot)
