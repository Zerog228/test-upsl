import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib as mpl

# Set dark theme for plots
mpl.style.use("dark_background")
sns.set_style("darkgrid", {"axes.facecolor": ".1", "grid.color": ".2", "axes.edgecolor": ".5"})

# Load data
@st.cache
def load_data():
    return pd.read_csv('shopping_trends.csv')

data = load_data()

# Page settings
st.title("🛍️ Shopping Trends Dashboard")
st.sidebar.title("⚙️ Opcje analizy")

# Filters
st.sidebar.markdown("### Filtry danych")
age_filter = st.sidebar.slider("Wiek klienta", int(data["Age"].min()), int(data["Age"].max()), (18, 60))
category_filter = st.sidebar.multiselect("Kategorie produktów", data["Category"].unique(), data["Category"].unique())
payment_method_filter = st.sidebar.multiselect("Sposoby płatności", data["Payment Method"].unique(), data["Payment Method"].unique())
season_filter = st.sidebar.multiselect("Sezony", data["Season"].unique(), data["Season"].unique())
gender_filter = st.sidebar.multiselect("Płeć klienta", data["Gender"].unique(), data["Gender"].unique())

# Filter data
filtered_data = data[(data["Age"] >= age_filter[0]) & 
                     (data["Age"] <= age_filter[1]) & 
                     (data["Category"].isin(category_filter)) &
                     (data["Payment Method"].isin(payment_method_filter)) &
                     (data["Season"].isin(season_filter)) &
                     (data["Gender"].isin(gender_filter))]

# Display data
st.write("### 📊 Filtrowane dane", filtered_data)

# Visualization
st.write("## 🔍 Analiza wizualna")

# Plot 1: Purchases by Category
st.write("### 📈 Liczba zakupów wg kategorii")
category_counts = filtered_data["Category"].value_counts()
fig, ax = plt.subplots(figsize=(12, 6))
sns.barplot(x=category_counts.index, y=category_counts.values, ax=ax, palette="Spectral")
ax.set_xlabel("Kategoria", fontsize=12, color="white")
ax.set_ylabel("Liczba zakupów", fontsize=12, color="white")
ax.set_title("Zakupy wg kategorii", fontsize=16, color="yellow")
ax.tick_params(axis='x', rotation=45, labelsize=10, colors="white")
ax.tick_params(axis='y', colors="white")
st.pyplot(fig)

# Plot 2: Average Purchase Amount by Season
st.write("### 💰 Średnia kwota zakupów wg sezonu")
season_mean = filtered_data.groupby("Season")["Purchase Amount (USD)"].mean()
fig, ax = plt.subplots(figsize=(12, 6))
sns.barplot(x=season_mean.index, y=season_mean.values, ax=ax, palette="cool")
ax.set_xlabel("Sezon", fontsize=12, color="white")
ax.set_ylabel("Średnia kwota zakupów (USD)", fontsize=12, color="white")
ax.set_title("Średnia kwota zakupów wg sezonu", fontsize=16, color="yellow")
ax.tick_params(colors="white")
st.pyplot(fig)

# Plot 3: Number of Customers by Age
st.write("### 👥 Liczba klientów wg wieku")
fig, ax = plt.subplots(figsize=(12, 6))
sns.histplot(filtered_data["Age"], bins=20, kde=True, color="lime", ax=ax)
ax.set_xlabel("Wiek", fontsize=12, color="white")
ax.set_ylabel("Liczba klientów", fontsize=12, color="white")
ax.set_title("Liczba klientów wg wieku", fontsize=16, color="yellow")
ax.tick_params(colors="white")
st.pyplot(fig)

# Plot 4: Payment Method by Category
st.write("### 🧾 Sposób płatności wg kategorii")
payment_category = filtered_data.groupby("Category")["Payment Method"].value_counts().unstack()
fig, ax = plt.subplots(figsize=(12, 6))
payment_category.plot(kind="bar", stacked=True, ax=ax, colormap="plasma", edgecolor="white")
ax.set_xlabel("Kategoria", fontsize=12, color="white")
ax.set_ylabel("Liczba transakcji", fontsize=12, color="white")
ax.set_title("Rozkład sposobów płatności wg kategorii", fontsize=16, color="yellow")
ax.legend(title="Sposób płatności", fontsize=10, facecolor=".1", edgecolor="white")
ax.tick_params(colors="white")
st.pyplot(fig)

# Plot 5: Total Purchase Amount by Age
st.write("### 📊 Łączna kwota zakupów wg wieku")
age_purchase = filtered_data.groupby("Age")["Purchase Amount (USD)"].sum()
fig, ax = plt.subplots(figsize=(12, 6))
age_purchase.plot(ax=ax, color="magenta", linewidth=2)
ax.set_xlabel("Wiek", fontsize=12, color="white")
ax.set_ylabel("Łączna kwota zakupów (USD)", fontsize=12, color="white")
ax.set_title("Łączna kwota zakupów w zależności od wieku", fontsize=16, color="yellow")
ax.grid(True, linestyle="--", alpha=0.5, color=".5")
ax.tick_params(colors="white")
st.pyplot(fig)

# Plot 6: Donut Chart for Purchases by Season
st.write("### 🕐 Liczba zakupów wg sezonu")
season_counts = filtered_data["Season"].value_counts()
fig, ax = plt.subplots(figsize=(10, 10))
colors = sns.color_palette("bright")
wedges, texts, autotexts = ax.pie(
    season_counts,
    autopct='%1.1f%%',
    startangle=90,
    colors=colors,
    wedgeprops={'edgecolor': 'white', 'linewidth': 1, 'width': 0.4}  # Donut hole
)
# Adjust text contrast
for text in texts + autotexts:
    text.set_color("white")
ax.set_title("Procentowy udział zakupów w sezonach", fontsize=16, color="yellow")
st.pyplot(fig)
