# Portfolio Optimization Project

This project implements several portfolio optimization strategies to maximize returns, minimize risk, and achieve specific financial goals. The strategies include the Sharpe Ratio Optimized Portfolio, Mean-Variance Optimization (MVO) Portfolio, Maximized Return Portfolio, Target Return Portfolio, and Target Risk Portfolio. The results are documented and visualized to aid in the decision-making process for portfolio management.

## Table of Contents

- [Requirements](#requirements)
- [Setup](#setup)
- [Scripts Overview](#scripts-overview)
  - [ychoose.py](#ychoosepy)
  - [yfin.py](#yfinpy)
  - [yxplanation.py](#yxplanationpy)
- [How to Run](#how-to-run)
- [License](#license)

## Requirements

- Python 3.x
- yfinance
- numpy
- pandas
- scipy
- matplotlib
- openpyxl

## Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/Quant-Portfolio.git
   cd Quant-Portfolio/Portfolio Optimization
2. Install the required Python packages:
pip install yfinance numpy pandas scipy matplotlib openpyxl

3. Activate the virtual environment (if applicable):
   For Unix/MacOS:
     source path_to_virtualenv/bin/activate
   For Windows:
     .\path_to_virtualenv\Scripts\activate
Scripts Overview
ychoose.py
Purpose: To filter and select stocks based on financial metrics such as market capitalization, profit margins, return on equity, and earnings growth.
Output: A list of selected stock symbols stored in selected_symbols.txt.

yfin.py
Purpose: To perform portfolio optimization using the selected stocks and compare the results to the S&P 500 benchmark.
Output: Visualization of cumulative returns for each optimized portfolio strategy.

yxplanation.py
Purpose: To summarize the portfolio strategies, detailing stock allocation, expected returns, and risks.
Output: An Excel file (Portfolio_Strategy_Summary.xlsx) summarizing the strategies and allocations.
How to Run
Run ychoose.py:

bash
Copy code
python ychoose.py
Process: This script processes a large set of stocks, filtering them based on defined financial metrics to narrow down a set of high-potential candidates for portfolio optimization. Output: The script outputs the selected stock symbols to selected_symbols.txt.
Run yfin.py:

bash
Copy code
python yfin.py
Process: This script performs portfolio optimization using the selected stocks. It employs various strategies to balance return and risk according to different financial theories and outputs visual comparisons to the S&P 500. Output: The script produces a chart of cumulative returns and displays the optimal weights for each strategy.
Run yxplanation.py:

bash
Copy code
python yxplanation.py
Process: This script generates an Excel file summarizing the portfolio strategies, including stock allocations, expected returns, and risks. Output: An Excel file (Portfolio_Strategy_Summary.xlsx) with a comprehensive overview of the portfolio strategies.
