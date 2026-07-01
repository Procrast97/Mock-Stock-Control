import pandas as pd
import openpyxl as xl
import numpy as np
import datetime as dt

today = dt.date.today()

curr_day = today.day
curr_month = today.month
curr_year = today.year

CURR_DOC_DATE = f"stock_report_{curr_day:02d}{curr_month:02d}{curr_year}.xlsx"


class DataManager:

    def __init__(self, file_path):
        try:
            self.xlsx_file = pd.ExcelFile(file_path + CURR_DOC_DATE)
            self.curr_stock_df = pd.read_excel(self.xlsx_file, sheet_name="Current Stock")
            self.restock_hist_df = pd.read_excel(self.xlsx_file, sheet_name="Restock History")
        except FileNotFoundError:
            raise FileNotFoundError(f"Could not find inventory file at location: {file_path}.\nPlease ensure the file path is correct.")
        except ValueError as e:
            raise ValueError(f"Sheet name issue - check 'Current Stock' and 'Restock History' exists: {e}.")
        """
        oos - 'out of stock'
        cs - 'critical stock'
        ls - 'low stock'
        """
        self.oos_columns = ["sku", "product_name", "supplier", "lead_time_days"]
        self.cs_columns = ["sku", "product_name", "supplier","days_of_stock_remaining", "lead_time_days"]
        self.ls_columns = ["sku", "product_name", "supplier", "days_of_stock_remaining", "last_restock_date"]



    def out_of_stock(self):
        zero_stock = self.curr_stock_df["current_stock"] == 0
        spec_items = self.curr_stock_df.loc[zero_stock, self.oos_columns].to_dict("records")
        return spec_items


    def critical_stock(self):
        crit_stock = self.curr_stock_df["days_of_stock_remaining"] < self.curr_stock_df["lead_time_days"]
        item_specs = self.curr_stock_df.loc[crit_stock, self.cs_columns].to_dict("records")
        return item_specs

    def low_stock(self):
        low_stock = self.curr_stock_df["current_stock"] < self.curr_stock_df["reorder_point"]
        not_critical = self.curr_stock_df["days_of_stock_remaining"] >= self.curr_stock_df["lead_time_days"]
        low_only = low_stock & not_critical
        low_items = self.curr_stock_df.loc[low_only, self.ls_columns].to_dict("records")
        return low_items

