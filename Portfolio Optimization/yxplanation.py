import yfinance as yf
import numpy as np
import pandas as pd
import scipy.optimize as sco
import datetime

# Define the end date as the current date
end_date = datetime.datetime.now().strftime('%Y-%m-%d')

# Load selected symbols from the file
with open("selected_symbols.txt", "r") as file:
    symbols = [line.strip() for line in file.readlines()]

# Download historical data for these stocks
data = yf.download(symbols, start='2020-01-01', end=end_date)

# Calculate monthly returns
monthly_returns = data['Adj Close'].resample('M').ffill().pct_change().dropna()

# Calculate the mean monthly returns and covariance matrix
mean_returns = monthly_returns.mean()
cov_matrix = monthly_returns.cov()

# Number of assets in the portfolio
num_assets = len(symbols)

# Initialize equal weights for the initial guess
initial_weights = np.array([1/num_assets] * num_assets)

# Constraints: weights must sum to 1
constraints = ({'type': 'eq', 'fun': lambda weights: np.sum(weights) - 1})

# Bounds: weights should be between 0 and 1 (no short selling)
bounds = tuple((0, 1) for asset in range(num_assets))

### Define objective functions for the different strategies
def portfolio_variance(weights, cov_matrix):
    return np.dot(weights.T, np.dot(cov_matrix, weights))

def sharpe_ratio(weights, mean_returns, cov_matrix, risk_free_rate=0.01):
    portfolio_return = np.sum(mean_returns * weights)
    portfolio_std_dev = np.sqrt(portfolio_variance(weights, cov_matrix))
    return -(portfolio_return - risk_free_rate) / portfolio_std_dev

def negative_portfolio_return(weights, mean_returns):
    return -np.sum(mean_returns * weights)

# Run the optimizations
opt_sharpe = sco.minimize(sharpe_ratio, initial_weights, args=(mean_returns, cov_matrix),
                          method='SLSQP', bounds=bounds, constraints=constraints)

opt_variance = sco.minimize(portfolio_variance, initial_weights, args=(cov_matrix,),
                            method='SLSQP', bounds=bounds, constraints=constraints)

opt_return = sco.minimize(negative_portfolio_return, initial_weights, args=(mean_returns,),
                          method='SLSQP', bounds=bounds, constraints=constraints)

# Define target return and target risk
target_return = 0.02
target_risk = 0.05

constraints_target_return = (
    {'type': 'eq', 'fun': lambda weights: np.sum(weights) - 1},
    {'type': 'eq', 'fun': lambda weights: np.sum(mean_returns * weights) - target_return}
)

constraints_target_risk = (
    {'type': 'eq', 'fun': lambda weights: np.sum(weights) - 1},
    {'type': 'ineq', 'fun': lambda weights: target_risk - np.sqrt(portfolio_variance(weights, cov_matrix))}
)

opt_target_return = sco.minimize(portfolio_variance, initial_weights, args=(cov_matrix,),
                                 method='SLSQP', bounds=bounds, constraints=constraints_target_return)

opt_target_risk = sco.minimize(negative_portfolio_return, initial_weights, args=(mean_returns,),
                               method='SLSQP', bounds=bounds, constraints=constraints_target_risk)

# Extract the optimal weights for each strategy
weights_sharpe = opt_sharpe.x
weights_variance = opt_variance.x  # MVO Portfolio
weights_return = opt_return.x
weights_target_return = opt_target_return.x
weights_target_risk = opt_target_risk.x

# Prepare data for the Excel table
strategies = ['Sharpe Ratio Optimized Portfolio', 
              'Mean-Variance Optimization (MVO) Portfolio', 
              'Maximized Return Portfolio', 
              'Target Return Portfolio', 
              'Target Risk Portfolio']

weights = [weights_sharpe, weights_variance, weights_return, weights_target_return, weights_target_risk]
expected_returns = [np.sum(weights_sharpe * mean_returns), 
                    np.sum(weights_variance * mean_returns), 
                    np.sum(weights_return * mean_returns), 
                    np.sum(weights_target_return * mean_returns), 
                    np.sum(weights_target_risk * mean_returns)]

expected_risks = [np.sqrt(portfolio_variance(weights_sharpe, cov_matrix)), 
                  np.sqrt(portfolio_variance(weights_variance, cov_matrix)), 
                  np.sqrt(portfolio_variance(weights_return, cov_matrix)), 
                  np.sqrt(portfolio_variance(weights_target_return, cov_matrix)), 
                  np.sqrt(portfolio_variance(weights_target_risk, cov_matrix))]

# Create a DataFrame for each strategy
df_list = []

for i, strategy in enumerate(strategies):
    df = pd.DataFrame({
        'Strategy': [strategy] * num_assets,
        'Stock': symbols,
        'Weight': weights[i]
    })
    df['Expected Return'] = expected_returns[i]
    df['Expected Risk (Std. Dev.)'] = expected_risks[i]
    df_list.append(df)

# Concatenate all DataFrames into one
final_df = pd.concat(df_list, ignore_index=True)

# Save the DataFrame to an Excel file
final_df.to_excel('Portfolio_Strategy_Summary.xlsx', index=False)

# Display a message when done
print("Excel file 'Portfolio_Strategy_Summary.xlsx' has been created.")
