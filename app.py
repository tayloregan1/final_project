import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt


@st.cache
def load_data(filename):
    return pd.read_csv(filename)


shark = load_data('cleaned_sharks.csv')
sharkattack_counts = load_data('sharkattack_counts.csv')

# def bar_plot(df, column1, column2): # Set x equal to place names
x = sharkattack_counts['Year']
bar_width = 0.75
fig, ax = plt.subplots()
# x-axis is place names, y-axis is attendance
ax.bar(x, sharkattack_counts['Amount of Shark Attacks'], width=bar_width, color='pink', edgecolor='blue')
# Set x-ticks to be place names
ax.set_xticks(x)
ax.set_xticks(sharkattack_counts['Year'])
plt.xticks(rotation=90)
# Set y-ticks to be more uniform plt.yticks(np.arange(1000000, 8500000, step=1000000)) # Add a grid
ax.grid(axis='y', linestyle='--')
# Add a title
plt.title('Amount of Shark Attacks per Year') # Add x label and y label
plt.xlabel('Year')
plt.ylabel('Amount of Shark Attacks')
# Display bar plot
st.pyplot(fig)

# sidebar
st.sidebar.title('Filter Data Here:')
st.header('Exploring Shark Attack Data')

min_year, max_year = st.sidebar.slider('Years to include:', 1961, 2020, (2000, 2020), 1)
filtered_df = shark.loc[(shark['Year'] <= max_year) & (shark['Year'] >= min_year)]

min_age, max_age = st.sidebar.slider('Ages to include:', 3, 87, (18, 35), 1)
filtered_df = filtered_df.loc[(shark['Age'] <= max_age) & (shark['Age'] >= min_age)]

countries = shark['Country'].unique()
countries_choice = st.sidebar.multiselect('Areas to include:', countries)
countries_choice_list = list(countries_choice)
filtered_df = filtered_df[shark['Country'].isin(countries_choice_list)]

sex = shark['Sex'].unique()
sex_choice = st.sidebar.multiselect('Sexes to include:', sex)
sex_choice_list = list(sex_choice)
filtered_df = filtered_df[shark['Sex'].isin(sex_choice_list)]

fatal = shark['Fatal==True'].unique()
fatal_choice = st.sidebar.multiselect('Types to include:', fatal)
fatal_choice_list = list(fatal_choice)
filtered_df = filtered_df[shark['Fatal==True'].isin(fatal_choice_list)]

st.dataframe(filtered_df)

st.header('Percent of Shark Attacks by Type of Attack')
unprov = len(shark[shark['Type'] == 'Unprovoked'])/len(shark)
prov = len(shark[shark['Type'] == 'Provoked'])/len(shark)
null = len(shark[shark['Type'].isnull()])/len(shark)
type_dictionary = {'Provoked': prov, 'Unprovoked': unprov, 'Other': null}
types = type_dictionary.keys()
freq = type_dictionary.values()
pie_chart = px.pie(values=freq, names=types, color=types, title='Pie Chart: Type of Attack')
st.plotly_chart(pie_chart)

# add labels to this graph
st.header("Amount of Shark Attacks per Year")
barplot = pd.pivot_table(sharkattack_counts, index=['Year'], values=['Amount of Shark Attacks'])
barplot.plot(kind='bar')
st.bar_chart(barplot)
