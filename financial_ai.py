import streamlit as st
import pandas as pd
import requests

# Your API key from FinancialModelingPrep
api_key = 's561z0EFing83mxqzi8E2J7s68CVbaXV'

# Get financial data for a company
def get_financials(ticker):
    try:
        url_income = f'https://financialmodelingprep.com/api/v3/financials/income-statement/{ticker}?apikey={api_key}'
        income_data = requests.get(url_income).json()

        url_balance = f'https://financialmodelingprep.com/api/v3/financials/balance-sheet-statement/{ticker}?apikey={api_key}'
        balance_data = requests.get(url_balance).json()

        url_cash_flow = f'https://financialmodelingprep.com/api/v3/financials/cash-flow-statement/{ticker}?apikey={api_key}'
        cashflow_data = requests.get(url_cash_flow).json()

        # Print the data to check structure
        st.write("Income Data:", income_data)
        st.write("Balance Data:", balance_data)
        st.write("Cash Flow Data:", cashflow_data)

        income_df = pd.DataFrame(income_data['financials'])
        balance_df = pd.DataFrame(balance_data['financials'])
        cashflow_df = pd.DataFrame(cashflow_data['financials'])

        return income_df, balance_df, cashflow_df
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        return None, None, None

# Analyze financials
def analyze_financials(income_df, balance_df, cashflow_df):
    income_df['Net Income'] = pd.to_numeric(income_df['Net Income'], errors='coerce')
    income_df['Revenue'] = pd.to_numeric(income_df['Revenue'], errors='coerce')
    balance_df['Total Debt'] = pd.to_numeric(balance_df['Total Debt'], errors='coerce')
    balance_df['Total Equity'] = pd.to_numeric(balance_df['Total Equity'], errors='coerce')
    cashflow_df['Free Cash Flow'] = pd.to_numeric(cashflow_df['Free Cash Flow'], errors='coerce')

    ratios = {}
    ratios['Net Profit Margin'] = income_df['Net Income'].iloc[0] / income_df['Revenue'].iloc[0]
    ratios['Debt-to-Equity Ratio'] = balance_df['Total Debt'].iloc[0] / balance_df['Total Equity'].iloc[0]
    ratios['Return on Equity (ROE)'] = income_df['Net Income'].iloc[0] / balance_df['Total Equity'].iloc[0]
    ratios['Current Ratio'] = balance_df['Total Assets'].iloc[0] / balance_df['Total Debt'].iloc[0]
    ratios['Free Cash Flow'] = cashflow_df['Free Cash Flow'].iloc[0]
    
    return ratios

# Classify investment decision
def classify_investment(ratios):
    investment_summary = "Investment is Good"
    if ratios['Net Profit Margin'] < 0.1:
        investment_summary = "Investment is Bad (Low Profit Margin)"
    elif ratios['Debt-to-Equity Ratio'] > 1.0:
        investment_summary = "Investment is Bad (Too Much Debt)"
    elif ratios['Return on Equity (ROE)'] < 0.15:
        investment_summary = "Investment is Bad (Low Return on Equity)"
    elif ratios['Current Ratio'] < 1.5:
        investment_summary = "Investment is Bad (Poor Liquidity)"
    elif ratios['Free Cash Flow'] < 0:
        investment_summary = "Investment is Bad (Negative Free Cash Flow)"

    return investment_summary

# Streamlit web app
st.title("AI Financial Investment Analyzer")
ticker = st.text_input("Enter a company ticker (e.g., TSLA for Tesla):")

if ticker:
    try:
        income_df, balance_df, cashflow_df = get_financials(ticker)
        if income_df is not None and balance_df is not None and cashflow_df is not None:
            ratios = analyze_financials(income_df, balance_df, cashflow_df)
            summary = classify_investment(ratios)
            
            st.subheader(f"Analysis for {ticker.upper()}:")
            st.write(f"Net Profit Margin: {ratios['Net Profit Margin']:.2f}")
            st.write(f"Debt-to-Equity Ratio: {ratios['Debt-to-Equity Ratio']:.2f}")
            st.write(f"Return on Equity: {ratios['Return on Equity (ROE)']:.2f}")
            st.write(f"Current Ratio: {ratios['Current Ratio']:.2f}")
            st.write(f"Free Cash Flow: {ratios['Free Cash Flow']:.2f}")
            st.write(f"Investment Decision: **{summary}**")
        else:
            st.error("Unable to retrieve or analyze the financials for the given company ticker. Please check the ticker and try again.")
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
