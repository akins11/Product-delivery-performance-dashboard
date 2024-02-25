from pandas import DataFrame, to_datetime
import calendar


def check_valid_month_name(month_name: str) -> list:
    """ 
    Check if the supplied month name if a valid month name.

    :params
    month_name: month name input.

    :return a list with a boolean value.
    """
    month_names = list(calendar.month_name[1:])
    
    if month_name not in month_names:
        return {"error": True, "message": f"Invalid month name, please enter a valid month name. Such as {', '.join(month_names)}"}
    else:
        return {"error": False, "message": "Valid month name"}
    

def clean_date(data: DataFrame, data_type: str) -> DataFrame:
    """ 
    """

    if data_type == "orders":
        date_cols = [
            "order_purchase_timestamp", 
            "order_approved_at", 
            "order_delivered_carrier_date", 
            "order_delivered_customer_date",
            "order_estimated_delivery_date"
        ]
    elif data_type == "customer":
        date_cols = ["order_purchase_timestamp"]
    else:
        date_cols = ["order_purchase_timestamp", "order_delivered_customer_date", "shipping_limit_date"]

    for date in date_cols:
        data[date] = to_datetime(data[date])
    
    return data


def filter_month(
        df: DataFrame, 
        date_var: str, 
        month_name: str, 
        leading_up_to_month: bool=False,
        drop_prev_year: bool=False
) -> dict:
    """
    :params
    df:
    date_var:
    month_name:
    leading_up_to_month:
    drop_prev_year:

    :return A dictionary containing boolean error and pandas dataframe.
    """
    # List of month names
    month_names = list(calendar.month_name[1:])
    # Create month dictionary with month id
    month_dic = {month_names[i] : i+1 for i in range(len(month_names))}

    try:
        # Get the period between the 12th month of 2017 and the inputed month.
        if leading_up_to_month:
            func_df = df[
                ((df[date_var].dt.year == 2017) & (df[date_var].dt.month == 12)) | (df[date_var].dt.month <= month_dic[month_name])
            ]
        else:
            func_df = df[df[date_var].dt.month == month_dic[month_name]]

        # Drop previous year (2017) data.
        if drop_prev_year:
            func_df = func_df[func_df[date_var].dt.year != 2017]

        return {"error": False, "message": " ", "data": func_df}
    
    except ValueError as e:
        return {
            "error": True,
            "message": f"An Error occured while filtering the data: {e}",
            "data": None
        }
    


