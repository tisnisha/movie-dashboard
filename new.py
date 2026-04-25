import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Movie Dashboard", page_icon="🎬", layout="wide")

df=pd.read_csv("tmdb_5000_movies.csv")

df=df[df['vote_average']>0]
df=df[df['vote_count']>100]

#filters
st.sidebar.title("Filters")
genre = st.sidebar.selectbox("Select Genre", ["All", "Action", "Comedy", "Drama", "Horror", "Romance", "Thriller"])
rating = st.sidebar.slider("Minimum Rating", 0.0, 10.0, 7.0)
if genre != "All":
    df = df[df['genres'].str.contains(genre, na=False)]

df = df[df['vote_average'] >= rating]

st.title("Movie Analytic Dashboard")

st.markdown("Explore movies from the TMDB dataset. Use the filters on the left to interact with the charts.")
st.metric("Total Movies", len(df))

st.subheader("Top 10 Highest Rated Movies")
top10= df.nlargest(10, 'vote_average')[['title','vote_average']]
fig = px.bar(top10, x="title", y="vote_average", color="vote_average", labels={"title": "Movie", "vote_average": "Rating"})
st.plotly_chart(fig)

st.subheader("Movies Released Per Year")
df['release_date']=pd.to_datetime(df['release_date'])
df['year']=df['release_date'].dt.year

movies_per_year =df.groupby('year')['title'].count().reset_index()
movies_per_year.columns = ['Year', 'Number of Movies']

fig2 = px.line(movies_per_year, x='Year', y='Number of Movies')
st.plotly_chart(fig2)

st.subheader("Budget vs Revenue")
df_money=df[(df['budget']>0) & (df['revenue']>0)]

fig3= px.scatter(df_money, x='budget', y='revenue', hover_name='title',labels={'budget': 'Budget ($)', 'revenue': 'Revenue ($)'})
st.plotly_chart(fig3)

