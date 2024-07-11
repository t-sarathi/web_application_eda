import pandas as pd

def drop_down(df):
    years = df['Year'].unique().tolist()
    years.sort()
    years.insert(0, 'overall')

    country = df['region'].dropna().unique().tolist()
    country.sort()
    country.insert(0, 'overall')
    return years,country

def fetch_medal_tally(df,year,country):
    medal_df=df.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'])
    flag=0
    if year=='overall' and country=="overall" :
        temp=medal_df
    if year=='overall' and country!="overall" :
        flag=1
        temp=medal_df[medal_df['region']==country]
    if year!='overall' and country=="overall" :
         temp=medal_df[medal_df['Year']==int(year)]
    if year!='overall' and country!="overall" :
        temp=medal_df[(medal_df['Year']==int(year)) & (medal_df['region']==country)]
    #when year all with specific country
    if flag==1:
         x=temp.groupby('Year').sum()[['Bronze','Gold','Silver']].sort_values('Year',ascending=True).reset_index()
    else:
         x=temp.groupby('region').sum()[['Bronze','Gold','Silver']].sort_values('Gold',ascending=False).reset_index()
    x['Total_medal']=x['Gold']+x['Silver']+x['Bronze']
    return x

def overall_analysis(df):
    No_of_year=df["Year"].nunique() - 1
    city=df["City"].nunique()
    sport=df["Sport"].nunique()
    event=df["Event"].nunique()
    region=df["region"].nunique()
    participant=df["Name"].nunique()
    return No_of_year,city,sport,event,region,participant

def year_wise_participating_nations(df):
    nation_overtime = pd.DataFrame(df.drop_duplicates(['Year', 'region'])['Year'].value_counts()).reset_index()
    nation_overtime.sort_values('Year', inplace=True)
    return nation_overtime

def participant_over_time(df):
    events_year = pd.DataFrame(df.drop_duplicates(['Year', 'Event'])['Year'].value_counts())
    events_year.sort_values('Year', inplace=True)
    events_year.reset_index(inplace=True)
    return events_year

def succesful_player(df,sport):
    temp=df.dropna(subset=["Medal"])
    temp=temp[temp['Sport']==sport]
    x=pd.DataFrame(temp['Name'].value_counts()).head(5).reset_index()
    x=x.rename(columns={'count':'Total Medal'})
    l = []
    for name in x['Name']:
        y = temp[temp['Name'] == name]['region'].tolist()
        l.append(y[0])
    x['Country'] = l
    return x

def country_wise_analysis(df,country):
    # Drop the none values
    df.dropna(subset=['Medal'])
    # drop the duplicates
    medal_df = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    # Create year wise medal tally
    newdf = medal_df[medal_df['region'] == country]
    newdf = newdf.groupby('Year').count()['Medal'].reset_index()
    # convert the datatype of year column
    newdf['Year'] = newdf['Year'].astype('int')
    return newdf

def countrywise_events(df,country):
    medal_df = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    x = medal_df.dropna(subset=['Medal'])
    y = x[x['region'] == country]
    return y


def athletes_age(df):
    athlete = df.drop_duplicates(subset=['Name', 'region'])
    x1 = athlete['Age'].dropna()
    x2 = athlete[athlete['Medal'] == 'Gold']['Age'].dropna()
    x3 = athlete[athlete['Medal'] == 'Silver']['Age'].dropna()
    x4 = athlete[athlete['Medal'] == 'Bronze']['Age'].dropna()

    return x1,x2,x3,x4


def men_vs_women(df):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])

    men = athlete_df[athlete_df['Sex'] == 'M'].groupby('Year').count()['Name'].reset_index()
    women = athlete_df[athlete_df['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index()

    final = men.merge(women, on='Year', how='left')
    final.rename(columns={'Name_x': 'Male', 'Name_y': 'Female'}, inplace=True)

    final.fillna(0, inplace=True)

    return final







