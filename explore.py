# /// script
# dependencies = [
#     "cpi==2.0.10",
#     "marimo",
#     "pandas==3.0.6",
#     "ty==0.0.82",
#     "xlrd==2.0.2",
# ]
# requires-python = ">=3.12"
# ///

import marimo

__generated_with = "0.24.2"
app = marimo.App(width="medium")


@app.cell
def _():
    from datetime import date, datetime
    from pathlib import Path

    import cpi
    import marimo as mo
    import pandas as pd

    return Path, cpi, pd


@app.cell
def _(cpi):
    cpi.update()

    def inflation_adjust(row):
        try:
            return cpi.inflate(
                row["Price"],
                row["Date"],
            )
        except:
            return row["Price"]

    return (inflation_adjust,)


@app.cell
def _(Path, inflation_adjust, pd):
    DIESEL_PRICE_DATA_FP = Path("./inputs/psw18vwall.xls")
    READ_COLUMNS = [
        "Date",
        "Weekly U.S. No 2 Diesel Retail Prices  (Dollars per Gallon)",
    ]
    COLUMN_RENAMES = ["Date", "Price"]

    weekly_diesel_prices = pd.read_excel(
        DIESEL_PRICE_DATA_FP,
        sheet_name="Data 1",
        skiprows=2,
    )
    weekly_diesel_prices = weekly_diesel_prices[READ_COLUMNS]
    weekly_diesel_prices.columns = COLUMN_RENAMES

    weekly_diesel_prices["inflation_adjusted_price"] = (
        weekly_diesel_prices.apply(inflation_adjust, axis=1)
    )
    return (weekly_diesel_prices,)


@app.cell
def _(OUTPUT_DIESEL_FP, pd):
    if OUTPUT_DIESEL_FP.exists():
        cached_inf_adjs = pd.read_csv(OUTPUT_DIESEL_FP)

    cached_inf_adjs
    return


@app.cell
def _(Path, weekly_diesel_prices):
    OUTPUT_DIESEL_FP = Path("./outputs/inflation_adjust_diesel.csv")
    weekly_diesel_prices.to_csv(OUTPUT_DIESEL_FP, index=False)
    weekly_diesel_prices.sort_values(
        "inflation_adjusted_price", ascending=False
    )
    return (OUTPUT_DIESEL_FP,)


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
