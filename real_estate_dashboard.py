import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from fpdf import FPDF

# Ensure required packages are installed
try:
    import streamlit
    import plotly
except ModuleNotFoundError:
    import os
    os.system('pip install streamlit plotly pandas numpy fpdf')

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

# Scenario Comparison Inputs
st.sidebar.header("Comparison Scenario")
alt_property_price = st.sidebar.number_input("Alternative Property Price", min_value=10000, value=350000, step=5000)
alt_down_payment = st.sidebar.slider("Alternative Down Payment (%)", 0, 100, 25)
alt_interest_rate = st.sidebar.slider("Alternative Loan Interest Rate (%)", 0.5, 10.0, 5.0, 0.1)

# Multi-scenario ROI Calculations
def calculate_roi(property_price, down_payment, loan_term, interest_rate, resale_growth, year_of_sale, num_units, rent_per_unit, vacancy_rate, tax_rate, manag_fee, repair_cost):
    down_payment_amount = property_price * (down_payment / 100)
    loan_amount = property_price - down_payment_amount
    monthly_interest_rate = (interest_rate / 100) / 12
    num_payments = loan_term * 12
    mortgage_payment = (loan_amount * monthly_interest_rate) / (1 - (1 + monthly_interest_rate) ** -num_payments)
    total_monthly_rent = num_units * rent_per_unit
    effective_rent = total_monthly_rent * (1 - vacancy_rate / 100)
    annual_rental_income = effective_rent * 12
    net_rental_income = annual_rental_income * (1 - ((tax_rate + manag_fee + repair_cost) / 100))
    resale_price = property_price * ((1 + resale_growth / 100) ** year_of_sale)
    capital_gains = resale_price - property_price
    total_annual_returns = net_rental_income + (capital_gains / year_of_sale)
    roi = (total_annual_returns / down_payment_amount) * 100
    return roi, resale_price, net_rental_income

roi_main, resale_price_main, net_rental_main = calculate_roi(property_price, down_payment, loan_term, interest_rate, resale_growth, year_of_sale, num_units, rent_per_unit, vacancy_rate, tax_rate, manag_fee, repair_cost)
roi_alt, resale_price_alt, net_rental_alt = calculate_roi(alt_property_price, alt_down_payment, loan_term, alt_interest_rate, resale_growth, year_of_sale, num_units, rent_per_unit, vacancy_rate, tax_rate, manag_fee, repair_cost)

# Multi-scenario Visualization
st.subheader("ROI Comparison")
data_comparison = pd.DataFrame({
    "Scenario": ["Main Investment", "Alternative Investment"],
    "ROI (%)": [roi_main, roi_alt],
    "Resale Price": [resale_price_main, resale_price_alt],
    "Net Rental Income": [net_rental_main, net_rental_alt],
})
fig_comparison = px.bar(data_comparison, x="Scenario", y=["ROI (%)", "Resale Price", "Net Rental Income"],
                         title="Comparison of Investment Scenarios",
                         barmode="group")
st.plotly_chart(fig_comparison)

# PDF Export with Scenario Comparison
if st.button("Download PDF Report"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, "Real Estate Investment Analysis Report", ln=True, align="C")
    pdf.ln(10)
    pdf.cell(200, 10, f"Main Investment ROI: {roi_main:.2f}%", ln=True)
    pdf.cell(200, 10, f"Alternative Investment ROI: {roi_alt:.2f}%", ln=True)
    pdf.cell(200, 10, f"Main Investment Resale Price: {currency} {resale_price_main:,.2f}", ln=True)
    pdf.cell(200, 10, f"Alternative Investment Resale Price: {currency} {resale_price_alt:,.2f}", ln=True)
    pdf.output("investment_analysis.pdf")
    st.success("PDF report with scenario comparison generated successfully!")
