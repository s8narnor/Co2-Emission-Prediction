
![co2_emission](https://github.com/user-attachments/assets/b375e6c3-006d-42b0-aade-77c9706a8321)

# 🌍 CO₂ Emissions Forecasting with Machine Learning

This project forecasts **future CO₂ emissions per capita** for countries around the world using machine learning. It combines historical environmental and economic indicators to predict carbon emissions over the next 15 years and is deployed using **Streamlit** for an interactive web interface.

---

## 🚀 Project Overview

- **Goal:** Predict and visualize future **CO₂ emissions per capita** based on country-level socio-economic and environmental indicators.
- **Technique:** Trained a **Random Forest Regressor** on historical data.
- **Forecast Period:** 15 years beyond the latest available data.
- **Interface:** Built a user-friendly **Streamlit app** featuring:
  - Country selection from 90+ options
  - CO₂ per capita forecast plot
  - Growth rate display for key features
  - Forecast table for the last 5 years

---

## 📊 Key Features Used

- `cereal_yield`
- `gni_per_cap`
- `en_per_cap`
- `pop_urb_aggl_perc`
- `prot_area_perc`
- `pop_growth_perc`
- `urb_pop_growth_perc`

---

## 🧠 ML Model

- **Model:** Random Forest Regressor (with hyperparameter tuning)
- **Target Variable:** `co2_per_cap` (CO₂ emissions per capita)
- **Training Data:** Cleaned multi-decade dataset for global countries
- **Forecasting Logic:** Projects each feature using **Compound Annual Growth Rate (CAGR)** before predicting future CO₂ values

---

## 🧪 How to Run Locally

1. Clone this repo:
   ```bash
   git clone https://github.com/s8narnor/Co2-Emission-Prediction.git
   cd Co2-Emission-Prediction

🌐 Demo
⚡ Coming soon: [Live Link]

📌 Future Improvements
- Support for real-time updates via API integration
- Incorporation of climate policy data
- Forecasting total CO₂ emissions (not just per capita)
- Downloadable reports or charts

