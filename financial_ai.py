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
        
        # Debugging output to check data structures
        st.write("Income Data:", income_data)
        st.write("Balance Data:", balance_data)
        st.write("Cash Flow Data:", cashflow_data)

        income_df = pd.DataFrame(income_data['financials'])
        balance_df = pd.DataFrame(balance_data['financials'])
        cashflow_df = pd.DataFrame(cashflow_data['financials'])

        # Check the contents of the DataFrames
        st.write("Income DataFrame:", income_df)
        st.write("Balance DataFrame:", balance_df)
        st.write("Cash Flow DataFrame:", cashflow_df)

        return income_df, balance_df, cashflow_df
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        return None, None, None
        
# Analyze financials
def analyze_financials(income_df, balance_df, cashflow_df):
    # Access values carefully and handle missing data
    net_income = pd.to_numeric(income_df['Net Income'].iloc[0], errors='coerce')
    revenue = pd.to_numeric(income_df['Revenue'].iloc[0], errors='coerce')

    total_debt = pd.to_numeric(balance_df.get('Total Debt', balance_df.get('Long Term Debt', 0)), errors='coerce')
    total_equity = pd.to_numeric(balance_df.get('Total Equity', 0), errors='coerce')
    total_assets = pd.to_numeric(balance_df.get('Total Assets', 1), errors='coerce')  # Prevent division by zero
    free_cash_flow = pd.to_numeric(cashflow_df.get('Free Cash Flow', 0), errors='coerce')

    # Check values before calculations
    st.write(f"Net Income: {net_income}, Revenue: {revenue}, Total Debt: {total_debt}, Total Equity: {total_equity}, Total Assets: {total_assets}, Free Cash Flow: {free_cash_flow}")

    ratios = {}
    ratios['Net Profit Margin'] = net_income / revenue if revenue > 0 else 0  # Changed condition to > 0
    ratios['Debt-to-Equity Ratio'] = total_debt / total_equity if total_equity > 0 else 0  # Changed condition to > 0
    ratios['Return on Equity (ROE)'] = net_income / total_equity if total_equity > 0 else 0  # Changed condition to > 0
    ratios['Current Ratio'] = total_assets / total_debt if total_debt > 0 else 0  # Changed condition to > 0
    ratios['Free Cash Flow'] = free_cash_flow

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
            
            # After calculating ratios
            st.subheader(f"Analysis for {ticker.upper()}:")
            net_profit_margin = ratios['Net Profit Margin'] if not pd.isna(ratios['Net Profit Margin']) else 0.00
            debt_to_equity_ratio = ratios['Debt-to-Equity Ratio'] if not pd.isna(ratios['Debt-to-Equity Ratio']) else 0.00
            return_on_equity = ratios['Return on Equity (ROE)'] if not pd.isna(ratios['Return on Equity (ROE)']) else 0.00
            current_ratio = ratios['Current Ratio'] if not pd.isna(ratios['Current Ratio']) else 0.00
            free_cash_flow = ratios['Free Cash Flow'] if not pd.isna(ratios['Free Cash Flow']) else 0.00

            st.write(f"Net Profit Margin: {net_profit_margin:.2f}")
            st.write(f"Debt-to-Equity Ratio: {debt_to_equity_ratio:.2f}")
            st.write(f"Return on Equity: {return_on_equity:.2f}")
            st.write(f"Current Ratio: {current_ratio:.2f}")
            st.write(f"Free Cash Flow: {free_cash_flow:.2f}")
            st.write(f"Investment Summary: {summary}")

        else:
            st.error("Unable to retrieve or analyze the financials for the given company ticker. Please check the ticker and try again.")
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
