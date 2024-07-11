import streamlit as st
import scipy
import pandas as pd
import initial,helper
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
from PIL import Image
import plotly.figure_factory as ff

df = pd.read_csv('athlete_events.csv')
region_df = pd.read_csv('noc_regions.csv')

df=initial.initially(df,region_df)

# Load your image
st.header("Olympics Data Analysis")
background_image = Image.open('—Pngtree—olympic day games background_996806.jpg')

# Display the image using st.image and adjust the layout
st.sidebar.image(background_image, use_column_width=True)
#Call the function which return me the dataframe


button1=st.sidebar.radio(
    'Select an option',
    ('Medal Tally','Overall Analysis','Country-wise Analysis')
)


if button1=="Medal Tally":
    st.subheader('**Medal** **Tally**')

    years,country=helper.drop_down(df)
    years=st.sidebar.selectbox('Select year',years)
    country=st.sidebar.selectbox('Select country',country)

    medal_tally=helper.fetch_medal_tally(df,years,country)
    st.table(medal_tally)

if button1=='Overall Analysis':
    No_of_year, city, sport, event, region, participant=helper.overall_analysis(df)

    col1,col2,col3=st.columns(3)
    with col1:
        st.header('Events')
        st.title(No_of_year)
    with col2:
        st.header('Cities')
        st.title(city)
    with col3:
        st.header('No of Sports')
        st.title(sport)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.header('Events')
        st.title(event)
    with col2:
        st.header('Countries')
        st.title(region)
    with col3:
        st.header('Athlete')
        st.title(participant)

    nation_over_time=helper.year_wise_participating_nations(df)
    st.title("Participating ___Nations___ over the ___years___")
    fig = px.line(nation_over_time, x="Year", y="count")
    fig.layout.yaxis.title = 'Participating Nations'
    st.plotly_chart(fig)

    events_year=helper.participant_over_time(df)
    st.title("Number of ___events___ over the ___years___")
    fig = px.line(events_year, x="Year", y="count", title='Events over Time')
    fig.layout.yaxis.title = 'Events'
    st.plotly_chart(fig)

    st.title("No of events in Each Sports(Over the Years)")
    fig,ax=plt.subplots(figsize=(20,20))
    x = df.drop_duplicates(['Year', 'Sport', 'Event'])
    sns.heatmap(x.pivot_table(index="Sport",columns='Year',
                                  values='Event',aggfunc='count').fillna(0).astype("int"),annot=True)

    fig = plt.gcf()
    st.pyplot(fig)
# Most successful players:
    sport=df['Sport'].unique().tolist()
    sport=st.selectbox('**Select** **Sport**',sport )
    st.title(f'Successfull players(5) in ___{sport}___')
    succesful_player=helper.succesful_player(df,sport)
    st.table(succesful_player)

# Country wise Analysis
if button1=='Country-wise Analysis':
    country = df['region'].dropna().unique().tolist()
    country.sort()
    country=st.sidebar.selectbox('Select the Country',country)
    st.title(f' Total Medals won by ___{country}___ over the Years')

    newdf=helper.country_wise_analysis(df,country)
    # plot the graph
    fig = px.line(newdf, x="Year", y="Medal")
    fig.layout.yaxis.title = 'Total medals---->'
    fig.layout.xaxis.title = 'Years ---->'
    st.plotly_chart(fig)


    st.subheader(f'Event wise Medals won by {country} over the years')
    y=helper.countrywise_events(df,country)
    fig1,ax=plt.subplots(figsize=(20,20))
    sns.heatmap(y.pivot_table(index="Sport", columns='Year', values='Event', aggfunc='count').fillna(0).astype("int"),
                annot=True)

    fig1 = plt.gcf()
    st.pyplot(fig1)

#Top 10 players:
    st.subheader(f"{country}'s top 10 Successful Athletes")
    top_players = y.groupby('Name').count()['Medal']
    top_players = pd.DataFrame(top_players)
    top_players=top_players.sort_values(by='Medal', ascending=False).head(10).reset_index()
    l = []
    for name in top_players['Name']:
        y = df[df['Name'] == name]['Event'].tolist()
        l.append(y[0])
    top_players['Event'] = l

    st.table(top_players)

#Athletes wise analysis:

# if button1=='Athelete wise Analysis':
 #   st.title('Distribution of Age')
  #  x1,x2,x3,x4=helper.athletes_age(df)
   # fig = ff.create_distplot([x1, x2, x3, x4], ['Age Distribution', 'Gold Medalist', 'Silver Medalist' ,
                                                #'Bronze Medalist'], show_hist=False, show_rug=False)
    #st.plotly_chart(fig)

    #Male and Female participation over the years
    #st.title("Men Vs Women Participation Over the Years")
    #final = helper.men_vs_women(df)
    #fig = px.line(final, x="Year", y=["Male", "Female"])
    #fig.update_layout(autosize=False, width=1000, height=600)
    #st.plotly_chart(fig)


