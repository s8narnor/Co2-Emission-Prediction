import streamlit as st
import pandas as pd
import numpy as np
import joblib

# Load model and data
rf_model = joblib.load("forecasting_co2_emmision.pkl")
data = pd.read_csv("data_cleaned.csv")

# Selected features
selected_features = [
    'cereal_yield', 'gni_per_cap', 'en_per_cap',
    'pop_urb_aggl_perc', 'prot_area_perc',
    'pop_growth_perc', 'urb_pop_growth_perc'
]

# Country list
country_list = [
    'AGO', 'ARE', 'ARG', 'AUS', 'AUT', 'BGD', 'BGR', 'BOL', 'BRA', 'CAN', 'CHE', 'CHL', 'CHN', 'CIV', 'CMR', 'COG',
    'COL', 'CRI', 'DEU', 'DNK', 'DOM', 'DZA', 'ECU', 'EGY', 'EMU', 'ESP', 'FIN', 'FRA', 'GBR', 'GHA', 'GRC', 'GTM',
    'HND', 'HUN', 'IDN', 'IND', 'IRL', 'ISR', 'ITA', 'JOR', 'JPN', 'KEN', 'KOR', 'LAC', 'LIC', 'LMC', 'LMY', 'MAR',
    'MEX', 'MIC', 'MNA', 'MOZ', 'MYS', 'NGA', 'NLD', 'NZL', 'PAK', 'PAN', 'PER', 'PHL', 'PRT', 'PRY', 'ROM', 'SAS',
    'SAU', 'SDN', 'SEN', 'SLV', 'SSA', 'SWE', 'SYR', 'TGO', 'THA', 'TUR', 'TZA', 'UMC', 'URY', 'USA', 'VEN', 'VNM',
    'WLD', 'ZAF', 'ZAR', 'ZMB', 'ARM', 'BLR', 'ECA', 'POL', 'RUS', 'UKR', 'UZB', 'YEM', 'CZE', 'ETH', 'KAZ', 'IRN'
]

# App setup
# Display image at the top
st.set_page_config(page_title="CO₂ Forecasting", layout="wide")

# Try loading banner image
try:
    st.image("co2_emission.jpg", use_container_width=True)  # Adjust path if needed
except FileNotFoundError:
    st.warning("Banner image not found. Skipping image display.")

st.title("🌱 Forecasting CO₂ Per Capita")

# Description of inputs
with st.expander("📘 Description of Features & Target Variable"):
    st.markdown("""
*🎯 Target (Dependent Variables):*
- `co2_percap` : CO₂ emissions per capita / CO₂ emissions per person (metric tons)

*📊 Features (Independent Variables):*
- `cereal_yield`: Cereal yield (kg per hectare)
- `gni_per_cap`: GNI per capita (Atlas \$)
- `en_per_cap`: Energy use per capita (kg of oil equivalent)
- `pop_urb_aggl_perc`: Population in urban agglomerations >1 million (%)
- `prot_area_perc`: Terrestrial protected areas (% of total land)
- `pop_growth_perc`: Population growth (annual %)
- `urb_pop_growth_perc`: Urban population growth (annual %)
    """)


# Sidebar: Select country
country = st.sidebar.selectbox("Select Country", sorted(country_list))
st.sidebar.markdown("---")

# Filter data for selected country
country_data = data[data['country'] == country].sort_values('year')

# Calculate growth rates (CAGR)
growth_rates = {}

start_year = country_data['year'].min()
end_year = country_data['year'].max()
years = end_year - start_year

if years > 0:
    for feature in selected_features:
        start_val = country_data[country_data['year'] == start_year][feature].values
        end_val = country_data[country_data['year'] == end_year][feature].values

        if len(start_val) and len(end_val):
            start_val, end_val = start_val[0], end_val[0]
            if start_val > 0 and end_val > 0 and np.isfinite(start_val) and np.isfinite(end_val):
                cagr = (end_val / start_val) ** (1 / years) - 1
                growth_rates[feature] = cagr

# Display growth rates in sidebar with bullet points
st.sidebar.markdown(f"### 📈 Growth Rates (CAGR) from {start_year} to {end_year}")
for feat, rate in growth_rates.items():
    sign = '+' if rate >= 0 else '−'
    st.sidebar.markdown(f"- **{feat}**: {sign}{abs(rate * 100):.2f}%")

# User inputs
st.subheader("Input Current Feature Values")
user_inputs = []
for feature in selected_features:
    default_val = float(country_data[feature].dropna().iloc[-1]) if not country_data[feature].dropna().empty else 1000.0
    val = st.number_input(f"{feature.replace('_', ' ').title()}", value=round(default_val, 2))
    user_inputs.append(val)

# Forecast year input
forecast_year = st.slider("Forecast Year", min_value=end_year+1, max_value=end_year+30, value=end_year+10)

# Predict
if st.button("Predict CO₂ per Capita"):
    if growth_rates:
        years_ahead = forecast_year - end_year
        future_vals = [val * ((1 + growth_rates.get(feat, 0.0)) ** years_ahead)
                       for val, feat in zip(user_inputs, selected_features)]
        input_array = np.array(future_vals).reshape(1, -1)
        pred = rf_model.predict(input_array)[0]
        st.success(f"Predicted CO₂ per Capita for {country} in {forecast_year}: **{pred:.2f} metric tons**")
    else:
        st.error("Cannot compute prediction due to missing growth rates.")



# Forecast future CO2 per capita
data_input = country_data[selected_features].dropna().iloc[-1].copy()
future_years = list(range(end_year + 1, end_year + 19))

forecast_results = []
for year in future_years:
    for feature in selected_features:
        growth = growth_rates.get(feature, 0.0)
        data_input[feature] *= (1 + growth)

    predicted = rf_model.predict(data_input.values.reshape(1, -1))[0]
    forecast_results.append({
        'year': year,
        'co2_percap': predicted
    })

# Convert to DataFrame
forecast_df = pd.DataFrame(forecast_results)

# Display forecast plot
st.title(f"📊 Forecasted CO₂ per Capita for {country}")
st.subheader("Using Growth Rate (CAGR)")
st.line_chart(forecast_df.set_index('year'))

st.subheader("Thank You!")

# Show forecast table for last 5 years in the forecast period
#st.subheader("📊 Last 5 Years of Forecast")
#st.dataframe(forecast_df.tail(5).reset_index(drop=True))
