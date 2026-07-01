import streamlit as st
import pandas as pd
import plotly.express as px
from utils.data_loader import load_and_clean_data

# -----------------------
# PAGE CONFIG
# -----------------------
st.set_page_config(
    page_title="Used Car Market Explorer",
    layout="wide"
)

# -----------------------
# LOAD DATA
# -----------------------
df = load_and_clean_data("data/cars.csv")

st.title("🚗 Used Car Market Explorer")

# -----------------------
# BASIC SAFETY CHECK
# -----------------------
st.sidebar.subheader("Data Quality Check")

st.sidebar.write({
    "rows": len(df),
    "missing_price": df["price"].isna().sum(),
    "missing_mileage": df["mileage"].isna().sum(),
    "missing_make": df["make"].isna().sum(),
    "missing_model": df["model"].isna().sum(),
})

# -----------------------
# SIDEBAR FILTERS
# -----------------------
st.sidebar.header("Filters")

# Make filter
make_options = ["All"] + sorted(df["make"].dropna().unique())
make = st.sidebar.selectbox("Make", make_options)

# Model filter (depends on make)
if make != "All":
    model_options = ["All"] + sorted(df[df["make"] == make]["model"].dropna().unique())
else:
    model_options = ["All"] + sorted(df["model"].dropna().unique())

model = st.sidebar.selectbox("Model", model_options)

# Year filter
year_min = int(df["year"].min())
year_max = int(df["year"].max())

year_range = st.sidebar.slider(
    "Year Range",
    year_min,
    year_max,
    (year_min, year_max)
)

# Price filter
price_min = int(df["price"].min())
price_max = int(df["price"].max())

price_range = st.sidebar.slider(
    "Price Range",
    price_min,
    price_max,
    (price_min, price_max)
)

# Mileage filter
mileage_min = int(df["mileage"].min())
mileage_max = int(df["mileage"].max())

mileage_range = st.sidebar.slider(
    "Mileage Range",
    mileage_min,
    mileage_max,
    (mileage_min, mileage_max)
)

# -----------------------
# APPLY FILTERS
# -----------------------
filtered = df.copy()

if make != "All":
    filtered = filtered[filtered["make"] == make]

if model != "All":
    filtered = filtered[filtered["model"] == model]

filtered = filtered[
    (filtered["year"] >= year_range[0]) &
    (filtered["year"] <= year_range[1]) &
    (filtered["price"] >= price_range[0]) &
    (filtered["price"] <= price_range[1]) &
    (filtered["mileage"] >= mileage_range[0]) &
    (filtered["mileage"] <= mileage_range[1])
]

# -----------------------
# KPIs
# -----------------------
st.subheader("Overview")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Vehicles", len(filtered))

col2.metric(
    "Avg Price",
    f"R {int(filtered['price'].mean()):,}" if len(filtered) > 0 else "N/A"
)

col3.metric(
    "Avg Mileage",
    f"{int(filtered['mileage'].mean()):,} km" if len(filtered) > 0 else "N/A"
)

col4.metric(
    "Avg Year",
    int(filtered["year"].mean()) if len(filtered) > 0 else "N/A"
)

# -----------------------
# DEAL SCORE (simple heuristic)
# -----------------------
filtered = filtered.copy()
filtered["deal_score"] = filtered["price"] / (filtered["mileage"] + 1)

# -----------------------
# PRICE DISTRIBUTION CHART
# -----------------------
st.subheader("Price Distribution")

if len(filtered) > 0:
    fig = px.histogram(
        filtered,
        x="price",
        nbins=30,
        title="Price Distribution"
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("No data available for selected filters.")

# -----------------------
# BEST DEALS
# -----------------------
st.subheader("Best Value Listings")

if len(filtered) > 0:
    best_deals = filtered.sort_values("deal_score").head(10)

    st.dataframe(
        best_deals[
            ["year", "make", "model", "variant", "price", "mileage", "dealer", "location", "url"]
        ],
        use_container_width=True
    )
else:
    st.info("No listings available.")

# -----------------------
# FULL RESULTS TABLE
# -----------------------
st.subheader(f"All Results ({len(filtered)})")

st.dataframe(
    filtered.sort_values("price"),
    use_container_width=True
)