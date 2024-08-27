import yfinance as yf
import pandas as pd

def get_sp500_symbols():
    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    tables = pd.read_html(url)
    sp500_table = tables[0]
    return sp500_table['Symbol'].tolist()

def get_stock_data(symbols):
    tickers = yf.Tickers(symbols)
    data = {symbol: tickers.tickers[symbol].info for symbol in symbols}
    return pd.DataFrame(data).T

def initial_filter(df):
    df['marketCap'] = pd.to_numeric(df['marketCap'], errors='coerce')
    df = df.dropna(subset=['marketCap'])
    large_caps = df[df['marketCap'] > 10**10]
    print(f"Stocks after initial filtering: {len(large_caps)}")
    return large_caps

def filter_by_financial_metrics(df, min_profit_margin=0.03, min_roe=0.05, min_earnings_growth=-0.05):
    df['profitMargins'] = pd.to_numeric(df['profitMargins'], errors='coerce')
    df['returnOnEquity'] = pd.to_numeric(df['returnOnEquity'], errors='coerce')
    df['earningsGrowth'] = pd.to_numeric(df['earningsGrowth'], errors='coerce')
    
    df = df.dropna(subset=['profitMargins', 'returnOnEquity', 'earningsGrowth'])
    
    df = df[(df['profitMargins'] > min_profit_margin) & (df['returnOnEquity'] > min_roe) & (df['earningsGrowth'] > min_earnings_growth)]
    
    print(f"Stocks after financial metrics filtering: {len(df)}")
    return df

def diversify_portfolio(df):
    # Ensure that key industries like Semiconductors are well represented
    df['industry'] = df['industry'].fillna('Unknown')
    
    # Increase the number of top companies taken from important industries like Semiconductors
    df['is_semiconductor'] = df['industry'].str.contains('Semiconductor', case=False, na=False)
    semiconductor_portfolio = df[df['is_semiconductor']].nlargest(10, 'marketCap')
    
    diversified_portfolio = df.groupby(['sector', 'industry'], group_keys=False).apply(lambda x: x.head(3)).reset_index(drop=True)
    
    # Before concatenating, ensure all columns are hashable
    for column in diversified_portfolio.columns:
        if isinstance(diversified_portfolio[column].iloc[0], list):
            diversified_portfolio[column] = diversified_portfolio[column].astype(str)
        if isinstance(semiconductor_portfolio[column].iloc[0], list):
            semiconductor_portfolio[column] = semiconductor_portfolio[column].astype(str)
    
    # Combine and remove duplicates
    diversified_portfolio = pd.concat([diversified_portfolio, semiconductor_portfolio]).drop_duplicates().reset_index(drop=True)
    
    print(f"Diversified portfolio contains {len(diversified_portfolio)} stocks")
    return diversified_portfolio

def select_top_10_by_industry(df):
    top_10_by_industry = df.groupby('industry', group_keys=False).apply(lambda x: x.nlargest(10, 'marketCap')).reset_index(drop=True)
    print(f"Top 10 by industry contains {len(top_10_by_industry)} stocks")
    return top_10_by_industry

def main():
    symbols = get_sp500_symbols()
    stock_data = get_stock_data(symbols)
    print(f"Total stocks fetched: {len(stock_data)}")

    filtered_data = initial_filter(stock_data)
    
    financially_filtered_data = filter_by_financial_metrics(filtered_data)
    diversified_portfolio = diversify_portfolio(financially_filtered_data)

    top_10_by_industry = select_top_10_by_industry(diversified_portfolio)

    # Extract symbols
    selected_symbols = top_10_by_industry['symbol'].tolist()  # Extract actual stock symbols
    print("\nSelected Symbols for Portfolio:")
    print(selected_symbols)

    with open("selected_symbols.txt", "w") as file:
        for symbol in selected_symbols:
            file.write(f"{symbol}\n")

if __name__ == "__main__":
    main()
