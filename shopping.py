import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib as mpl
import plotly.express as px
import plotly.graph_objects as go

# Set dark theme for plots and background
mpl.style.use("dark_background")
sns.set_style("darkgrid")

# Custom CSS for dark background in Streamlit
st.markdown(
    """
    <style>
    .main {background-color: black; color: white;}
    .sidebar .sidebar-content {background-color: #333333; color: white;}
    </style>
    """,
    unsafe_allow_html=True
)

# Wczytaj dane
@st.cache
def load_data():
    return pd.read_csv('shopping_trends.csv')

data = load_data()

# Ustawienia strony
st.set_page_config(page_title="Shopping Trends Dashboard", layout="wide", initial_sidebar_state="expanded")
st.title("🛍️ Shopping Trends Dashboard")
st.sidebar.title("⚙️ Opcje analizy")

# Filtry
st.sidebar.markdown("### Filtry danych")
age_filter = st.sidebar.slider("Wiek klienta", int(data["Age"].min()), int(data["Age"].max()), (18, 60))
category_filter = st.sidebar.multiselect("Kategorie produktów", data["Category"].unique(), data["Category"].unique())
payment_method_filter = st.sidebar.multiselect("Sposoby płatności", data["Payment Method"].unique(), data["Payment Method"].unique())
season_filter = st.sidebar.multiselect("Sezony", data["Season"].unique(), data["Season"].unique())
gender_filter = st.sidebar.multiselect("Płeć klienta", data["Gender"].unique(), data["Gender"].unique())

# Filtruj dane
filtered_data = data[(data["Age"] >= age_filter[0]) & 
                     (data["Age"] <= age_filter[1]) & 
                     (data["Category"].isin(category_filter)) &
                     (data["Payment Method"].isin(payment_method_filter)) &
                     (data["Season"].isin(season_filter)) &
                     (data["Gender"].isin(gender_filter))]

# Wyświetlanie danych
st.write("### 📊 Filtrowane dane", filtered_data)

# Wykres 1: Zakupy wg kategorii
st.write("### 📈 Liczba zakupów wg kategorii")
category_counts = filtered_data["Category"].value_counts()
fig = px.bar(
    x=category_counts.index,
    y=category_counts.values,
    color=category_counts.index,
    labels={"x": "Kategoria", "y": "Liczba zakupów"},
    title="Zakupy wg kategorii",
    color_discrete_sequence=px.colors.sequential.Sunset,
)
fig.update_layout(title_font=dict(size=20, color="cyan"), paper_bgcolor="black", plot_bgcolor="black")
st.plotly_chart(fig)

# Wykres 2: Średnia kwota zakupów wg sezonu
st.write("### 💰 Średnia kwota zakupów wg sezonu")
season_mean = filtered_data.groupby("Season")["Purchase Amount (USD)"].mean()
fig = px.bar(
    x=season_mean.index,
    y=season_mean.values,
    color=season_mean.index,
    labels={"x": "Sezon", "y": "Średnia kwota zakupów (USD)"},
    title="Średnia kwota zakupów wg sezonu",
    color_discrete_sequence=px.colors.cyclical.IceFire,
)
fig.update_layout(title_font=dict(size=20, color="cyan"), paper_bgcolor="black", plot_bgcolor="black")
st.plotly_chart(fig)

# Wykres 3: Liczba klientów wg wieku
st.write("### 👥 Liczba klientów wg wieku")
fig = px.histogram(
    filtered_data, x="Age", nbins=20, color_discrete_sequence=["lime"], marginal="box",
    title="Liczba klientów wg wieku",
)
fig.update_layout(title_font=dict(size=20, color="cyan"), paper_bgcolor="black", plot_bgcolor="black")
st.plotly_chart(fig)

# Wykres 4: Sposób płatności wg kategorii
st.write("### 🧾 Sposób płatności wg kategorii")
payment_category = filtered_data.groupby("Category")["Payment Method"].value_counts().unstack()
fig = px.bar(
    payment_category,
    barmode="stack",
    labels={"value": "Liczba transakcji", "index": "Kategoria"},
    title="Rozkład sposobów płatności wg kategorii",
    color_discrete_sequence=px.colors.qualitative.Dark24,
)
fig.update_layout(title_font=dict(size=20, color="cyan"), paper_bgcolor="black", plot_bgcolor="black")
st.plotly_chart(fig)

# Wykres 5: Łączna kwota zakupów wg wieku
st.write("### 📊 Łączna kwota zakupów wg wieku")
age_purchase = filtered_data.groupby("Age")["Purchase Amount (USD)"].sum()
fig = go.Figure(
    go.Scatter(
        x=age_purchase.index, 
        y=age_purchase.values, 
        mode="lines+markers", 
        line=dict(color="magenta", width=2),
    )
)
fig.update_layout(
    title="Łączna kwota zakupów w zależności od wieku",
    xaxis_title="Wiek",
    yaxis_title="Łączna kwota zakupów (USD)",
    title_font=dict(size=20, color="cyan"),
    paper_bgcolor="black",
    plot_bgcolor="black",
)
st.plotly_chart(fig)

# Wykres 6: Liczba zakupów wg sezonu
st.write("### 🕐 Liczba zakupów wg sezonu")
season_counts = filtered_data["Season"].value_counts()
fig = px.pie(
    names=season_counts.index,
    values=season_counts.values,
    color_discrete_sequence=px.colors.sequential.Pastel,
    title="Procentowy udział zakupów w sezonach",
)
fig.update_layout(title_font=dict(size=20, color="cyan"), paper_bgcolor="black")
st.plotly_chart(fig)
