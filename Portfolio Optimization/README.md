# Portfolio Optimization Project
Portfolio Optimization Project
This project implements several portfolio optimization strategies to maximize returns, minimize risk, and achieve specific financial goals. The strategies include the Sharpe Ratio Optimized Portfolio, Mean-Variance Optimization (MVO) Portfolio, Maximized Return Portfolio, Target Return Portfolio, and Target Risk Portfolio. The results are documented and visualized to aid in the decision-making process for portfolio management.

Table of Contents
Requirements
Setup
Scripts Overview
How to Run
Detailed Strategy Explanations
Results
Requirements
Python 3.x
The following Python packages:
yfinance
numpy
pandas
scipy
matplotlib
openpyxl
Setup
Clone the repository:

bash
Copy code
git clone https://github.com/your-username/Quant-Portfolio.git
cd Quant-Portfolio/Portfolio Optimization
Install the required Python packages:

bash
Copy code
pip install yfinance numpy pandas scipy matplotlib openpyxl
Activate the virtual environment (if applicable):

bash
Copy code
source path_to_virtualenv/bin/activate  # For Unix/MacOS
.\path_to_virtualenv\Scripts\activate  # For Windows
Scripts Overview
ychoose.py:

Purpose: To filter and select stocks based on financial metrics such as market capitalization, profit margins, return on equity, and earnings growth.
Output: A list of selected stock symbols stored in selected_symbols.txt.
yfin.py:

Purpose: To perform portfolio optimization using the selected stocks and compare the results to the S&P 500 benchmark.
Output: Visualization of cumulative returns for each optimized portfolio strategy.
yxplanation.py:

Purpose: To summarize the portfolio strategies, detailing stock allocation, expected returns, and risks.
Output: An Excel file (Portfolio_Strategy_Summary.xlsx) summarizing the strategies and allocations.
How to Run
Run ychoose.py:

bash
Copy code
python ychoose.py
Process: This script processes a large set of stocks, filtering them based on defined financial metrics to narrow down a set of high-potential candidates for portfolio optimization.
Output: The script outputs the selected stock symbols to selected_symbols.txt.
Run yfin.py:

bash
Copy code
python yfin.py
Process: This script performs portfolio optimization using the selected stocks. It employs various strategies to balance return and risk according to different financial theories and outputs visual comparisons to the S&P 500.
Output: The script produces a visualization of cumulative returns comparing each strategy to the S&P 500.
Run yxplanation.py:

bash
Copy code
python yxplanation.py
Process: This script generates an Excel file summarizing the stock allocation, expected returns, and risks for each strategy, providing an easily interpretable overview of the portfolio management process.
Output: The script outputs Portfolio_Strategy_Summary.xlsx, which includes a detailed breakdown of each strategy.
Detailed Strategy Explanations
Sharpe Ratio Optimized Portfolio:

Objective: To maximize the portfolio’s Sharpe Ratio, which measures risk-adjusted return.
Method: This strategy focuses on achieving the highest return for a given level of risk by optimizing the balance between expected return and standard deviation.
Application: Suitable for investors looking to maximize their returns relative to the amount of risk they are willing to take.
Mean-Variance Optimization (MVO) Portfolio:

Objective: To minimize portfolio variance (i.e., risk) while achieving a desired level of expected return.
Method: By solving the classic MVO problem, the strategy allocates capital to minimize the portfolio’s overall risk.
Application: Ideal for risk-averse investors who aim to reduce the uncertainty of returns.
Maximized Return Portfolio:

Objective: To maximize the expected return of the portfolio, regardless of risk.
Method: This strategy focuses on selecting the highest-performing stocks based on past returns without considering the associated risks.
Application: Suitable for aggressive investors who prioritize high returns and are less concerned about potential volatility.
Target Return Portfolio:

Objective: To achieve a specific target return while minimizing risk.
Method: This strategy adjusts the portfolio to meet a predetermined return target, balancing between high and low-risk assets to minimize volatility.
Application: Useful for investors with a specific return goal in mind who want to minimize the risk involved in achieving that return.
Target Risk Portfolio:

Objective: To achieve the highest possible return for a given level of risk.
Method: This strategy tailors the portfolio to a specific risk threshold, focusing on maximizing returns within the acceptable risk level.
Application: Ideal for investors who have a defined risk tolerance and want to optimize returns within those constraints.
Results
Excel Summary: The Portfolio_Strategy_Summary.xlsx file provides a comprehensive overview of each strategy, including:

Stock Allocations: How stocks are distributed in each portfolio.
Expected Returns: The anticipated returns for each strategy.
Expected Risk: The calculated risk (standard deviation) for each strategy.
Visualizations: The scripts generate plots that compare the cumulative returns of each portfolio strategy against the S&P 500 benchmark, illustrating the effectiveness of the optimizations over the period from January 2020 to the current date.
