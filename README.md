# 🌍 Oil War Impact Analysis 

## Project Overview
This project analyzes how geopolitical conflicts affect global oil prices, countries economic vulnerability, and consumer petrol price inflation. The goal is to help **policy makers, energy analysts, and economic organizations** understand which countries are most at risk and how fuel crises impact populations.

---

## Problem Statement
- **Core Problem:** How do geopolitical conflicts affecting oil supply impact fuel prices, economies, and vulnerable populations?
- 
- **Questions:**  
  - Which countries will suffer the most economically?  
  - Which populations face petrol affordability crises?  
  - Which countries are most resilient?

---

## Technologies & Tools
- **Python:** pandas, matplotlib, seaborn, Streamlit  
- **Database:** PostgreSQL 

---

##  Process

1. **Data Engineering**  
   - Load CSVs into PostgreSQL tables  
   - Clean and standardize datasets (country names, dates, numeric columns)  
   - Create views for vulnerability, exposure, and price changes  

2. **Data Analysis (Python)**  
   - Calculate **Vulnerability Score** for countries (Oil Import %, GDP Impact, Petrol Price Increase)  
   - Calculate **Exposure Score** combining multiple risk factors (Oil Import %, Inflation, Currency Pressure, GDP Impact)  
   - Classify countries into risk levels: Low, Medium, High, Critical  

3. **Visualizations**  
   - Brent Oil Prices trend during conflicts  
   - Vulnerability Score & Exposure Score by country  
   - Petrol price increase and Oil Import dependency  
   - Oil Import vs Petrol Price Increase scatter chart  

4. **Insights**  
   - Events like Brent $104, Stock crashes, and $150 warnings caused the largest spikes  
   - Average Brent price rose from **$90.66 → $93.94** during conflict  
   - Strait of Hormuz closure triggered largest oil spike  
   - Countries importing **>80% of oil** faced largest fuel inflation  
   - South Asia, especially **Sri Lanka**, is most vulnerable  
   - Oil exporters remained relatively stable  
   - Pakistan experienced higher inflation alongside rising oil prices  

---

## Streamlit report
- **KPI :** Average Vulnerability Score & Exposure Score  
- **Charts & Visuals:**  
  - Brent Oil Prices Trend  
  - Top Countries by Vulnerability & Exposure Scores  
  - Oil Import vs Petrol Price Increase  
  - Petrol Price Increase & Oil Import Dependency  

## Takeaways

- Governments and analysts can prioritize interventions for vulnerable countries
- Identify populations most affected by fuel crises
- Monitor oil price shocks and assess economic exposure
