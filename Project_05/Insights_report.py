# app.py
import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
import seaborn as sns

# -------------------------------
# Page Config
# -------------------------------
st.set_page_config(page_title="Oil War Analysis ", layout="wide")

# -------------------------------
#  Connect to PostgreSQL
# -------------------------------
engine = create_engine(
    "postgresql+psycopg2://postgres:YourNewPassword123@localhost:5432/oil_war_analysis"
)

# -------------------------------
#  Load CSVs into DataFrames
# -------------------------------
@st.cache_data
def load_data():
    country = pd.read_csv("country_impact.csv")
    oil = pd.read_csv("crude_oil_daily.csv")
    petrol = pd.read_csv("petrol_prices_comparison.csv")
    pros = pd.read_csv("pros_cons_analysis.csv")
    events = pd.read_csv("war_timeline.csv")
    
    # Push to SQL
    country.to_sql("country_impact", engine, if_exists="replace", index=False)
    oil.to_sql("oil_prices", engine, if_exists="replace", index=False)
    petrol.to_sql("petrol_prices", engine, if_exists="replace", index=False)
    pros.to_sql("pros_cons", engine, if_exists="replace", index=False)
    events.to_sql("war_events", engine, if_exists="replace", index=False)
    
    # Merge country + petrol data for calculations
    df = country.merge(
        petrol[['Country', 'Pct_Increase']], on='Country', how='left'
    )
    
    # Map inflation and currency to numeric scores
    df['inflation_core'] = df['Inflation_Risk'].map({
        'Low':10,'Moderate':20,'High':30,'Very High':40,'Extreme':50
    })
    df['currency_score'] = df['Currency_Pressure'].map({
        'Low':10,'Moderate':20,'High':30,'Severe':40,'Extreme':50
    })
    df['gdp_impact'] = abs(df['GDP_Impact_Pct'])
    
    # Vulnerability Score
    df["vulnerability_score"] = (
        df["Oil_Import_Pct"]*0.4 +
        abs(df["GDP_Impact_Pct"])*0.3 +
        df["Pct_Increase"]*0.3
    )
    
    # Exposure Score
    df["exposure_score"] = (
        df["Oil_Import_Pct"] * 0.3 +
        df["inflation_core"] * 0.2 +
        df["currency_score"] * 0.2 +
        df["gdp_impact"] * 0.3
    )
    
    # Risk Level
    def classify(score):
        if score > 60:
            return "Critical Risk"
        elif score > 40:
            return "High Risk"
        elif score > 20:
            return "Medium Risk"
        else:
            return "Low Risk"
    df["risk_level"] = df["exposure_score"].apply(classify)
    
    # Oil prices
    oil['Date'] = pd.to_datetime(oil['Date'])
    
    return df, oil

df, oil_df = load_data()

# -------------------------------
#  Title Page with Button
# -------------------------------
st.title("🌍 Oil War Impact Analysis")
st.markdown(
    """
    **Welcome!** This dashboard visualizes the impact of geopolitical conflicts on oil prices, country vulnerability, and petrol price inflation.
    
    Click the button below to view **Insights & Charts**.
    """
)

if st.button(" Insights "):
    
    # -------------------------------
    #  KPIs
    # -------------------------------
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Average Vulnerability Score", f"{df['vulnerability_score'].mean():.2f}")
    with col2:
        st.metric("Average Exposure Score", f"{df['exposure_score'].mean():.2f}")
    
    # -------------------------------
    #  Oil Prices Trend Chart
    # -------------------------------
    st.subheader(" Brent Oil Prices During Conflict")
    fig1, ax1 = plt.subplots(figsize=(14,6))
    ax1.plot(oil_df["Date"], oil_df["Brent_USD"], marker="o", color="blue", linestyle="-")
    ax1.set_xlabel("Date")
    ax1.set_ylabel("Brent (USD)")
    ax1.set_title("Brent Oil Prices Trend")
    plt.xticks(rotation=45)
    st.pyplot(fig1)
    
    # -------------------------------
    #  Vulnerability Score Chart
    # -------------------------------
    st.subheader(" Top Countries by Vulnerability Score")
    top_vul = df.sort_values("vulnerability_score", ascending=False).head(10)
    fig2, ax2 = plt.subplots(figsize=(14,6))
    sns.barplot(data=top_vul, x="vulnerability_score", y="Country", palette="Oranges_r", ax=ax2)
    ax2.set_xlabel("Vulnerability Score")
    ax2.set_ylabel("Country")
    st.pyplot(fig2)
    
    # -------------------------------
    #  Exposure Score Chart
    # -------------------------------
    st.subheader(" Top Countries by Exposure Score")
    top_exp = df.sort_values("exposure_score", ascending=False).head(10)
    fig3, ax3 = plt.subplots(figsize=(14,6))
    sns.barplot(data=top_exp, x="exposure_score", y="Country", palette="Greens_r", ax=ax3)
    ax3.set_xlabel("Exposure Score")
    ax3.set_ylabel("Country")
    st.pyplot(fig3)
    
    # -------------------------------
    #  Scatter: Oil Import vs Petrol Price Increase
    # -------------------------------
    st.subheader(" Oil Import Dependency vs Petrol Price Increase")
    fig4, ax4 = plt.subplots(figsize=(12,6))
    ax4.scatter(df["Oil_Import_Pct"], df["Pct_Increase"], color="red")
    for i in range(len(df)):
        ax4.text(df["Oil_Import_Pct"][i]+0.5, df["Pct_Increase"][i]+0.2, df["Country"][i], fontsize=8)
    ax4.set_xlabel("Oil Import %")
    ax4.set_ylabel("Petrol Price Increase %")
    st.pyplot(fig4)
    
    # -------------------------------
    #  Additional Chart 1: Petrol Price Increase
    # -------------------------------
    st.subheader(" Country vs Petrol Price Increase")
    Largest_price_increase = df.sort_values("Pct_Increase", ascending=False)
    fig5, ax5 = plt.subplots(figsize=(14,6))
    sns.barplot(data=Largest_price_increase, x="Pct_Increase", y="Country", palette="coolwarm", ax=ax5)
    ax5.set_xlabel("Petrol Price Increase (%)")
    ax5.set_ylabel("Country")
    st.pyplot(fig5)
    
    # -------------------------------
    #  Additional Chart 2: Oil Import Dependency
    # -------------------------------
    st.subheader(" Country Oil Import Dependency")
    fig6, ax6 = plt.subplots(figsize=(14,6))
    sns.barplot(data=df, x="Oil_Import_Pct", y="Country", palette="Greens", ax=ax6)
    ax6.set_xlabel("Oil Import Dependency (%)")
    ax6.set_ylabel("Country")
    st.pyplot(fig6)
    
    # -------------------------------
    #  Insights Section
    # -------------------------------
    st.subheader("📝 Key Insights")
    st.markdown("""
    1. Events like Brent $104, Stock crashes, and $150 warning caused the largest spikes in oil prices.  
    2. Average Brent price increased from 90.66 (pre-conflict) to 93.94 (during conflict).  
    3. Strait of Hormuz closure triggered the largest oil price spike.  
    4. Countries importing oil > 80% faced the biggest fuel inflation.  
    5. South Asia is the most vulnerable region, especially Sri Lanka.  
    6. Oil exporters remained relatively stable.  
    7. Inflation rate in Pakistan increased alongside oil prices compared to other countries.
    """)
