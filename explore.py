# /// script
# dependencies = [
#     "cpi==2.1.0",
#     "marimo",
#     "mcp==2.2.0",
#     "pandas==3.0.6",
#     "requests==2.34.2",
#     "ty==0.0.82",
#     "xlrd==2.0.2",
# ]
# requires-python = ">=3.12"
# ///

import marimo

__generated_with = "0.25.0"
app = marimo.App(width="medium")


@app.cell
def _():
    from datetime import date, datetime
    from pathlib import Path

    import cpi
    import marimo as mo
    import pandas as pd
    import requests

    return Path, cpi, pd


@app.cell
def _(cpi):
    cpi.update()
    return


@app.cell
def _(cpi):
    def inflation_adjust(row):
        try:
            return round(
                cpi.inflate(
                    row["Price"],
                    row["Date"],
                ),
                3,
            )
        except:
            return row["Price"]

    return (inflation_adjust,)


@app.cell
def _(Path, pd):
    DIESEL_PRICE_DATA_FP = Path("./inputs/psw18vwall.xls")
    DIESEL_HISTORICAL_PRICES_DATA_URL = (
        "https://www.eia.gov/petroleum/gasdiesel/xls/psw18vwall.xls"
    )

    READ_COLUMNS = [
        "Date",
        "Weekly U.S. No 2 Diesel Retail Prices  (Dollars per Gallon)",
    ]
    COLUMN_RENAMES = ["Date", "Price"]

    weekly_diesel_raw_prices = pd.read_excel(
        DIESEL_HISTORICAL_PRICES_DATA_URL,
        sheet_name="Data 1",
        skiprows=2,
    )
    weekly_diesel_raw_prices.to_csv(DIESEL_PRICE_DATA_FP)
    return COLUMN_RENAMES, READ_COLUMNS, weekly_diesel_raw_prices


@app.cell
def _(Path, pd):
    OUTPUT_DIESEL_FP = Path("./outputs/inflation_adjust_diesel.csv")
    if OUTPUT_DIESEL_FP.exists():
        cached_inf_adjs = pd.read_csv(OUTPUT_DIESEL_FP, parse_dates=["Date"])
        # cached_inf_adjs["Date"] = pd.to_datetime(cached_inf_adjs["Date"])
        cached_inf_adjs = {
            row["Date"]: row["inflation_adjusted_price"]
            for _, row in cached_inf_adjs.iterrows()
        }
    else:
        cached_inf_adjs = dict()
    return OUTPUT_DIESEL_FP, cached_inf_adjs


@app.cell
def _(
    COLUMN_RENAMES,
    READ_COLUMNS,
    cached_inf_adjs,
    inflation_adjust,
    weekly_diesel_raw_prices,
):
    def inflation_adjust_cached(row, cached=cached_inf_adjs):
        # if row["Date"] in cached:
        #     return cached.get(row["Date"])
        return inflation_adjust(row)

    weekly_diesel_prices = weekly_diesel_raw_prices[READ_COLUMNS]
    weekly_diesel_prices.columns = COLUMN_RENAMES

    weekly_diesel_prices["inflation_adjusted_price"] = (
        weekly_diesel_prices.apply(inflation_adjust_cached, axis=1)
    )
    weekly_diesel_prices["price_rank"] = weekly_diesel_prices[
        "inflation_adjusted_price"
    ].rank(ascending=False)
    return (weekly_diesel_prices,)


@app.cell
def _(OUTPUT_DIESEL_FP, weekly_diesel_prices):
    weekly_diesel_prices.to_csv(OUTPUT_DIESEL_FP, index=False)
    weekly_diesel_prices.sort_values(
        "inflation_adjusted_price", ascending=False
    )
    return


@app.cell
def _(weekly_diesel_prices):
    weekly_diesel_prices.sort_values("Date", ascending=False).to_json(
        "./peakdiesel-app/static/weekly_diesel_prices.json",
        orient="records",
        date_format="iso",
    )
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
