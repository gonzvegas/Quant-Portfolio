import yfinance as yf
import numpy as np
import pandas as pd
import scipy.optimize as sco
import matplotlib.pyplot as plt
import datetime

# Define the end date as the current date
end_date = datetime.datetime.now().strftime('%Y-%m-%d')

# List of stock symbols you're interested in
symbols = ['AAPL', 'MSFT', 'GOOGL', 'AMZN']

# Download historical data for these stocks
data = yf.download(symbols, start='2020-01-01', end=end_date)

# Download S&P 500 data
sp500_data = yf.download('^GSPC', start='2020-01-01', end=end_date)

# Calculate monthly returns
monthly_returns = data['Adj Close'].resample('ME').ffill().pct_change().dropna()
sp500_returns = sp500_data['Adj Close'].resample('ME').ffill().pct_change().dropna()

# Calculate the mean monthly returns
mean_returns = monthly_returns.mean()

# Calculate the covariance matrix of monthly returns
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
    return -(portfolio_return - risk_free_rate) / portfolio_std_dev  # Negate for minimization

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

# Calculate portfolio returns for each optimization strategy
sharpe_portfolio_returns = np.dot(monthly_returns, weights_sharpe)
variance_portfolio_returns = np.dot(monthly_returns, weights_variance)
return_portfolio_returns = np.dot(monthly_returns, weights_return)
target_return_portfolio_returns = np.dot(monthly_returns, weights_target_return)
target_risk_portfolio_returns = np.dot(monthly_returns, weights_target_risk)

# Align index with the S&P 500 returns
aligned_index = sp500_returns.index

# Reindex portfolio returns to align with the S&P 500 returns
sharpe_portfolio_returns = pd.Series(sharpe_portfolio_returns, index=aligned_index)
variance_portfolio_returns = pd.Series(variance_portfolio_returns, index=aligned_index)
return_portfolio_returns = pd.Series(return_portfolio_returns, index=aligned_index)
target_return_portfolio_returns = pd.Series(target_return_portfolio_returns, index=aligned_index)
target_risk_portfolio_returns = pd.Series(target_risk_portfolio_returns, index=aligned_index)

# Calculate cumulative returns for each portfolio and the benchmark
cumulative_sharpe = (1 + sharpe_portfolio_returns).cumprod()
cumulative_variance = (1 + variance_portfolio_returns).cumprod()  # This represents the MVO Portfolio
cumulative_return = (1 + return_portfolio_returns).cumprod()
cumulative_target_return = (1 + target_return_portfolio_returns).cumprod()
cumulative_target_risk = (1 + target_risk_portfolio_returns).cumprod()
cumulative_sp500 = (1 + sp500_returns).cumprod()

# Plot cumulative returns with the S&P 500 benchmark
plt.figure(figsize=(12, 8))
plt.plot(cumulative_sharpe, label='Sharpe Ratio Optimized Portfolio', color='blue', linestyle='-', linewidth=2)
plt.plot(cumulative_variance, label='Mean-Variance Optimization (MVO) Portfolio', color='green', linestyle='-', linewidth=2)
plt.plot(cumulative_return, label='Maximized Return Portfolio', color='orange', linestyle='-', linewidth=2)
plt.plot(cumulative_target_return, label='Target Return Portfolio', color='red', linestyle='-', linewidth=2)
plt.plot(cumulative_target_risk, label='Target Risk Portfolio', color='purple', linestyle='-', linewidth=2)
plt.plot(cumulative_sp500, label='S&P 500 Benchmark', linestyle='--', color='black', linewidth=2)
plt.title('Cumulative Returns of Optimized Portfolios vs S&P 500 Benchmark')
plt.xlabel('Date')
plt.ylabel('Cumulative Return')
plt.legend()
plt.show()

# Display the optimal weights for each strategy
print("Optimal Weights for Mean-Variance Optimization (MVO) Portfolio:", weights_variance)
print("Expected Return of MVO Portfolio:", np.sum(weights_variance * mean_returns))
print("Expected Risk (Std. Dev.) of MVO Portfolio:", np.sqrt(portfolio_variance(weights_variance, cov_matrix)))

print("Optimal Weights for Maximizing Sharpe Ratio:", weights_sharpe)
print("Optimal Weights for Minimizing Variance:", weights_variance)
print("Optimal Weights for Maximizing Return:", weights_return)
print("Optimal Weights for Target Return with Minimum Risk:", weights_target_return)
print("Optimal Weights for Target Risk with Maximum Return:", weights_target_risk)
