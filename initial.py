import streamlit as st
import pandas as pd

def initially(df,region_df):
    #import the data set
    df = pd.read_csv("../sample1/athlete_events.csv")
    region_csv = pd.read_csv("../sample1/noc_regions.csv")

    #we only focus on summer olympics, drop winter rows
    df = df[df['Season'] == 'Summer']
    #merge two data frame
    df = df.merge(region_csv, on='NOC', how='right')
    # drop duplicates
    df.drop_duplicates(inplace=True)
    # perform one hot encoding on medals column
    df = pd.concat([df, pd.get_dummies(df['Medal'])], axis=1)
    return df
































