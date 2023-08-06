# ReportGeneration
Trades report generation: task 3.

## Description of the task:
For all the hours of a given day, is displayed on the terminal the number of trades, the total quantity sold, 
the total quantity bought and finally the pnl value. 
The total pnl (sum across all delivery hours) for the trading day should be displayed.

## How to run it
The solution for the task is provided as a python package with easy execution.

- First, install the package `pip install challenge.report-generation`
- Run the command for generating a new report for a given trader_id and date. A database URL needs to be provided as well.
- Command example:  `report_generation.py --SQL-db-url postgresql://user:password@postgres:5432/postgresDB --trader-id trader1 --date 2022/01/03`
- The database URL and the trader_ir parameters are mandatory. If a date is not provided, the current date will be taken.