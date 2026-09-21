# /// script
# dependencies = [
#     "cpi==2.0.10",
#     "marimo",
#     "mcp==2.2.0",
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
    return


@app.cell
def _(cpi):
    def inflation_adjust(row):
        print(f"Here: {row}")
        try:
            return cpi.inflate(
                row["Price"],
                row["Date"],
            )
        except:
            return row["Price"]

    return (inflation_adjust,)


@app.cell
def _(Path, pd):
    DIESEL_PRICE_DATA_FP = Path("./inputs/psw18vwall.xls")
    READ_COLUMNS = [
        "Date",
        "Weekly U.S. No 2 Diesel Retail Prices  (Dollars per Gallon)",
    ]
    COLUMN_RENAMES = ["Date", "Price"]

    weekly_diesel_raw_prices = pd.read_excel(
        DIESEL_PRICE_DATA_FP,
        sheet_name="Data 1",
        skiprows=2,
    )
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
        if row["Date"] in cached:
            return cached.get(row["Date"])
        return inflation_adjust(row)

    weekly_diesel_prices = weekly_diesel_raw_prices[READ_COLUMNS]
    weekly_diesel_prices.columns = COLUMN_RENAMES

    weekly_diesel_prices["inflation_adjusted_price"] = (
        weekly_diesel_prices.apply(inflation_adjust_cached, axis=1)
    )
    return (weekly_diesel_prices,)


@app.cell
def _(OUTPUT_DIESEL_FP, weekly_diesel_prices):
    weekly_diesel_prices.to_csv(OUTPUT_DIESEL_FP, index=False)
    weekly_diesel_prices.sort_values(
        "inflation_adjusted_price", ascending=False
    )
    return


if __name__ == "__main__":
    app.run()
