import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import scipy.stats as stats

# set page configuration
st.set_page_config(page_title="Shark Attacks and Sea Level",
                   initial_sidebar_state="expanded")

st.image('shark.jpeg')

# function to load in CSV files
@st.cache
def load_data(filename):
    return pd.read_csv(filename)


# load in CSV files
shark = load_data('cleaned_sharks.csv')
sharkattack_counts = load_data('sharkattack_counts.csv')
northamerica = load_data('northamerica.csv')
df_to_graph = load_data('median_sea_levels.csv')


st.markdown('Welcome! Here you can explore some data related to shark attacks and sea levels. To get started, '
            'select some parameters on the sidebar to view shark attack data in the table below.')


st.header('Exploring Shark Attack Data')

# add title to sidebar
st.sidebar.title('Filter Data Here:')

# create slider for years and assign slider endpoints to min_year and max_year
min_year, max_year = st.sidebar.slider('Years to include:', 1961, 2020, (2000, 2020), 1)
# filter dataframe to include years between minimum and maximum years from slider
filtered_df = shark.loc[(shark['Year'] <= max_year) & (shark['Year'] >= min_year)]

# create slider for ages and assign slider endpoints to min_age and max_age
del filtered_df['Unnamed: 0']
min_age, max_age = st.sidebar.slider('Ages to include:', 3, 87, (18, 35), 1)
# filter dataframe to include ages between minimum and maximum ages from slider
filtered_df = filtered_df.loc[(shark['Age'] <= max_age) & (shark['Age'] >= min_age)]

# create unique series of countries
countries = shark['Country'].unique()
# create multiselect option in sidebar to choose countries from sorted series of unique countries
countries_choice = st.sidebar.multiselect('Areas to include:', sorted(countries))
# convert the countries selected in sidebar to a list
countries_choice_list = list(countries_choice)
# filter dataframe to display only rows with countries in the list of selected countries
filtered_df = filtered_df[shark['Country'].isin(countries_choice_list)]

# create unique series of sexes
sex = shark['Sex'].unique()
# create multiselect option in sidebar to choose sexes from series of unique sexes
sex_choice = st.sidebar.multiselect('Sexes to include:', sex)
# convert the sexes selected in sidebar to a list
sex_choice_list = list(sex_choice)
# filter dataframe to display only rows with the sexes in the list of selected sexes
filtered_df = filtered_df[shark['Sex'].isin(sex_choice_list)]

provoked = shark['Type'].unique()
provoked_choice = st.sidebar.multiselect('Provoked or Unprovoked?:', provoked)
provoked_choice_list = list(provoked_choice)
filtered_df = filtered_df[shark['Type'].isin(provoked_choice_list)]

# create unique series of fatality types
fatal = shark['Fatal==True'].unique()
# create multiselect option in sidebar to choose fatality types from series of unique fatality types
fatal_choice = st.sidebar.multiselect('Fatality:', fatal)
# convert the fatality types selected in sidebar to a list
fatal_choice_list = list(fatal_choice)
# filter dataframe to display only rows with the fatality types in the list of selected fatality types
filtered_df = filtered_df[shark['Fatal==True'].isin(fatal_choice_list)]

st.sidebar.markdown("After you're done changing the parameters, click the button that says CLICK ME to see a table.")

if st.button("CLICK ME"):
    st.dataframe(filtered_df)
    st.markdown(f'Above is a table showing the shark attacks that fit the adjusted parameters in the sidebar. '
                f'If you do not see any entries in the table, there are not any shark attacks that fit the criteria '
                f'you entered. Try adjusting them and see if the table changes. '
                f'You can click on the column names to filter the table by that column.')
    st.markdown('Areas currently selected:')
    # display the countries currently selected in the sidebar
    for x in countries_choice_list:
        st.write(x)

    # display percent of global shark attacks that occurred in the countries selected
    st.markdown(f'<p style="font-family:Monospace; color:#9271AF; font-size: 16px;">'
                'Percent of global shark attacks that occurred in these areas: </p>',
                unsafe_allow_html=True)
    st.write(f"{len(filtered_df)/len(shark)*100:.2f}%")

    # with the sidebar parameters, display percent of shark attacks that are fatal
    st.markdown(f'<p style="font-family:Monospace; color:#9271AF; font-size: 16px;">'
                'Percent of shark attacks that are fatal with parameters selected: </p>',
                unsafe_allow_html=True)
    if len(filtered_df) > 0:
        st.write(f"{(len(filtered_df[filtered_df['Fatal==True'] == 1])/len(filtered_df)*100):.2f}%")
    else:
        st.write('There are no entries in the dataframe!')

    st.markdown("Keep changing parameters to see these percentages move!")


# pie chart
st.header('Percent of Shark Attacks by Type of Attack')
unprov = len(shark[shark['Type'] == 'Unprovoked'])/len(shark)
prov = len(shark[shark['Type'] == 'Provoked'])/len(shark)
null = len(shark[shark['Type'].isnull()])/len(shark)
type_dictionary = {'Provoked': prov, 'Unprovoked': unprov, 'Other': null}
types = type_dictionary.keys()
freq = type_dictionary.values()
pie_chart = px.pie(values=freq, names=types, color=types, title='Pie Chart: Type of Attack')
st.plotly_chart(pie_chart)
st.markdown('This pie chart shows the percentage of attacks that are classified as provoked, unprovoked, '
            'or some other type. As we can see, a lot of shark attacks are unprovoked! '
            'Interact with the legend to filter the pie chart.')


# bar chart
st.header('Number of Shark Attacks Per Year')
x = sharkattack_counts['Year']
bar_width = 0.75
fig, ax = plt.subplots()
ax.bar(x, sharkattack_counts['Amount of Shark Attacks'], width=bar_width, color='#9271AF')
years_for_xticks = [1961, 1970, 1980, 1990, 2000, 2010, 2020]
ax.set_xticks(years_for_xticks)
plt.xticks(rotation=90)
ax.grid(axis='y', linestyle='--')
plt.xlabel('Year')
plt.ylabel('Number of Shark Attacks')
ax.set_facecolor('#F1EF7D')
fig.set_facecolor('#F1EF7D')
st.pyplot(fig)
st.markdown("This bar chart shows the number of shark attacks as time progresses. "
            "This number decreases at first, but starts to pick up again in the late 1970s. "
            "Could this increase in shark attacks have anything to do with climate change? ")


# scatterplot
st.header('Number of Shark Attacks vs. Median Sea Level')
fig2, ax2 = plt.subplots()
ax2.set_facecolor('#F1EF7D')
fig2.set_facecolor('#F1EF7D')
sns.scatterplot(data=northamerica, x="Median Sea Level", y="Case Number Count", color='#9271AF')
st.pyplot(plt.gcf())
st.markdown("This is a scatterplot that shows the number of shark attacks per year at the median yearly sea level. "
            "We can see a slight trend up and to the right, so there is some association between between number "
            "of shark attacks and median sea level. Let's put a number on this association.")


# heatmap
st.header('Correlation Coefficient Heatmap')
fig3, ax3 = plt.subplots()
ax3.set_facecolor('#F1EF7D')
fig3.set_facecolor('#F1EF7D')
new_df = northamerica.filter(['Median Sea Level', 'Case Number Count'], axis=1)
correlation_coefficients = np.corrcoef(new_df, rowvar=False)
sns.heatmap(correlation_coefficients, annot=True, cmap='Pastel1')
plt.xticks(np.arange(2)+0.5, new_df, rotation=45)
plt.yticks(np.arange(2)+0.5, new_df.columns, rotation=0)
st.pyplot(plt.gcf())
st.markdown("This is a heatmap that shows the correlation coefficients between the number of shark attacks and the "
            "monthly median sea level. With a correlation coefficient of 0.35, the number of shark attacks and monthly median sea level "
            "have a slightly strong positive relationship. We can confirm if this relationship is significant with a "
            "hypothesis test.")

st.header('Hypothesis Test')
a = 0.05

high_level = np.quantile(new_df['Median Sea Level'], .75)
low_level = np.quantile(new_df['Median Sea Level'], .25)

high_sea_level = new_df[new_df['Median Sea Level'] >= high_level]['Case Number Count']
low_sea_level = new_df[new_df['Median Sea Level'] <= low_level]['Case Number Count']
t_statistics, p_value = stats.ttest_ind(high_sea_level, low_sea_level, equal_var=False)
reject_H0 = p_value < a
st.write(f'alpha level: {a}')
st.write(f'p-value: {p_value}')
st.write(f'Is the relationship significant? (True=Yes): {reject_H0}')
st.markdown('Since the p-value is less than alpha, we reject the null hypothesis. '
            'This means there is a significant difference between low and high sea levels in terms '
            'of the number of shark attacks that occur!')

st.header('Thanks for reading :) come back soon')
