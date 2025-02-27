import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Ensure required packages are installed
try:
    import streamlit
    import plotly
except ModuleNotFoundError:
    import os
    os.system('pip install streamlit plotly pandas numpy')

# Dashboard Title
st.title("Real Estate Investment ROI Simulator")

# Sidebar Inputs
st.sidebar.header("Investment Parameters")
property_type = st.sidebar.selectbox("Property Type", ["Apartment", "House", "Commercial", "Land"])
currency = st.sidebar.selectbox("Currency", ["USD", "EUR", "GBP", "CNY"])
property_price = st.sidebar.number_input("Property Price", min_value=10000, value=300000, step=5000)
down_payment = st.sidebar.slider("Down Payment (%)", 0, 100, 20)
loan_term = st.sidebar.slider("Loan Term (Years)", 5, 30, 20)
interest_rate = st.sidebar.slider("Loan Interest Rate (%)", 0.5, 10.0, 4.0, 0.1)
num_units = st.sidebar.number_input("Number of Apartments / Assets", 1, 50, 1)
rent_per_unit = st.sidebar.number_input("Monthly Rent per Unit", min_value=100, value=1200, step=50)
vacancy_rate = st.sidebar.slider("Vacancy Rate (%)", 0, 20, 5)
tax_rate = st.sidebar.slider("Property & Other Taxes (%)", 0, 20, 10)
manag_fee = st.sidebar.slider("Management Fee (% of Rent)", 0, 20, 8)
repair_cost = st.sidebar.slider("Repair Cost (% of Rent)", 0, 10, 3)
resale_growth = st.sidebar.slider("Annual Appreciation (%)", -5, 10, 3)
year_of_sale = st.sidebar.slider("Year of Sale", 1, loan_term, 10)
benchmark_return = st.sidebar.slider("S&P 500 Expected Return (%)", 0, 15, 7)

# Calculations
down_payment_amount = property_price * (down_payment / 100)
loan_amount = property_price - down_payment_amount
monthly_interest_rate = (interest_rate / 100) / 12
num_payments = loan_term * 12
mortgage_payment = (loan_amount * monthly_interest_rate) / (1 - (1 + monthly_interest_rate) ** -num_payments)

total_monthly_rent = num_units * rent_per_unit
effective_rent = total_monthly_rent * (1 - vacancy_rate / 100)
annual_rental_income = effective_rent * 12
net_rental_income = annual_rental_income * (1 - ((tax_rate + manag_fee + repair_cost) / 100))

# Capital Gains & ROI Calculations
resale_price = property_price * ((1 + resale_growth / 100) ** year_of_sale)
capital_gains = resale_price - property_price
total_annual_returns = net_rental_income + (capital_gains / year_of_sale)
roi = (total_annual_returns / down_payment_amount) * 100

# DataFrame for Visualization
data = pd.DataFrame({
    "Year": np.arange(1, year_of_sale + 1),
    "Resale Value": [property_price * ((1 + resale_growth / 100) ** i) for i in range(1, year_of_sale + 1)],
    "Cumulative Net Rental Income": np.cumsum([net_rental_income] * year_of_sale),
})

# Visualization
st.subheader("ROI Analysis")
st.metric("Total Monthly Rent", f"{currency} {total_monthly_rent:,.2f}")
st.metric("Net Annual Rental Income", f"{currency} {net_rental_income:,.2f}")
st.metric("Resale Price at Year {year_of_sale}", f"{currency} {resale_price:,.2f}")
st.metric("ROI on Down Payment (%)", f"{roi:.2f}%")

fig = px.line(data, x="Year", y=["Resale Value", "Cumulative Net Rental Income"],
              title="Resale Value & Cumulative Rental Income Over Time",
              labels={"value": "Value in " + currency, "variable": "Metric"})
st.plotly_chart(fig)

# Benchmark Comparison
benchmark_growth = down_payment_amount * ((1 + benchmark_return / 100) ** year_of_sale)
st.metric("S&P 500 Equivalent Growth", f"{currency} {benchmark_growth:,.2f}")
