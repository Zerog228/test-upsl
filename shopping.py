import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Wczytaj dane
@st.cache
def load_data():
    return pd.read_csv('shopping_trends.csv')

data = load_data()

# Ustawienia strony
st.title("Shopping Trends Dashboard")
st.sidebar.title("Opcje analizy")

# Filtry
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
st.write("### Filtrowane dane", filtered_data)

# Wykresy
st.write("## Analiza wizualna")

# Wykres 1: Zakupy wg kategorii
st.write("### Liczba zakupów wg kategorii")
category_counts = filtered_data["Category"].value_counts()
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x=category_counts.index, y=category_counts.values, ax=ax, palette="viridis")
ax.set_xlabel("Kategoria")
ax.set_ylabel("Liczba zakupów")
ax.set_title("Zakupy wg kategorii")
ax.tick_params(axis='x', rotation=45)
st.pyplot(fig)

# Wykres 2: Średnia kwota zakupów wg sezonu
st.write("### Średnia kwota zakupów wg sezonu")
season_mean = filtered_data.groupby("Season")["Purchase Amount (USD)"].mean()
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x=season_mean.index, y=season_mean.values, ax=ax, palette="coolwarm")
ax.set_xlabel("Sezon")
ax.set_ylabel("Średnia kwota zakupów (USD)")
ax.set_title("Średnia kwota zakupów wg sezonu")
st.pyplot(fig)

# Wykres 3: Liczba klientów wg wieku
st.write("### Liczba klientów wg wieku")
fig, ax = plt.subplots(figsize=(10, 6))
sns.histplot(filtered_data["Age"], bins=20, kde=True, color="purple", ax=ax)
ax.set_xlabel("Wiek")
ax.set_ylabel("Liczba klientów")
ax.set_title("Liczba klientów wg wieku")
st.pyplot(fig)

# Wykres 4: Sposób płatności wg kategorii
st.write("### Sposób płatności wg kategorii")
payment_category = filtered_data.groupby("Category")["Payment Method"].value_counts().unstack()
fig, ax = plt.subplots(figsize=(10, 6))
payment_category.plot(kind="bar", stacked=True, ax=ax, colormap="Set2")
ax.set_xlabel("Kategoria")
ax.set_ylabel("Liczba transakcji")
ax.set_title("Rozkład sposobów płatności wg kategorii")
ax.legend(title="Sposób płatności")
st.pyplot(fig)

# Wykres 5: Łączna kwota zakupów wg wieku
st.write("### Łączna kwota zakupów wg wieku")
age_purchase = filtered_data.groupby("Age")["Purchase Amount (USD)"].sum()
fig, ax = plt.subplots(figsize=(10, 6))
age_purchase.plot(ax=ax, color="darkgreen", linewidth=2)
ax.set_xlabel("Wiek")
ax.set_ylabel("Łączna kwota zakupów (USD)")
ax.set_title("Łączna kwota zakupów w zależności od wieku")
ax.grid(True)
st.pyplot(fig)

# Wykres 6: Liczba zakupów wg sezonu
st.write("### Liczba zakupów wg sezonu")
season_counts = filtered_data["Season"].value_counts()
fig, ax = plt.subplots(figsize=(8, 8))
season_counts.plot(kind="pie", autopct='%1.1f%%', ax=ax, colors=sns.color_palette("pastel"))
ax.set_ylabel("")
ax.set_title("Procentowy udział zakupów w sezonach")
st.pyplot(fig)
