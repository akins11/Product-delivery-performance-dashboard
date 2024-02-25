from pandas import DataFrame
from numpy import where
from logic.global_function import filter_month
from logic.duration_function import create_time_diff


def seller_count(data: DataFrame, date_var: str, month_name: str) -> dict:
    """ 
    :params
    data: App data with seller's information
    date_var:
    month_name:

    :return a dictionary
    """
    
    if "seller_id" not in data.columns:
        return {
            "error": True,
            "message": "Data supplied does not have a seller id; make sure orders table is accurately joined with seller table",
            "overall_seller_count": None,
            "seller_count": None,
            "percentage": None
        }
    
    # Overall number of sellers in the data
    overall_seller_count = data["seller_id"].nunique()

    # Total number of active sellers in the selected month
    func_dict = filter_month(data, date_var, month_name, False, True)

    if func_dict["error"] == False:
        seller_count = func_dict["data"]["seller_id"].nunique()

        percentage = round(seller_count / overall_seller_count * 100)
    else:
        seller_count = None
        percentage = None

    return {
        "error": False, 
        "message": "", 
        "overall_seller_count": overall_seller_count, 
        "seller_count": seller_count, 
        "percentage": percentage
    }




def top_sellers_order_deadline(data: DataFrame, date_var: str, month_name:str, top: int=5) -> dict:
    """ 
    :params
    data: a dataframe filtered by month.
    top:
    :return a dictionary
    """

    # Total number of active sellers in the selected month
    func_dict = filter_month(data, date_var, month_name, False, True)
    error_dict = {
            "error": True,
            "message": f"An error occured while calculating time difference: {func_dict['message']}",
            "data": None,
            "avg_days": None
        }

    if func_dict["error"]:
        return error_dict
    else:
        # Days difference of actual vs limit.
        func_dict = create_time_diff(func_dict["data"], "shipping_limit_date", "order_delivered_customer_date", "day")

        if func_dict["error"]:
            return error_dict
        else:
            # Get the average time difference 
            func_df = (
                func_dict["data"]
                .groupby("seller_id")["period"]
                .agg("mean")
                .reset_index()
                .sort_values(by="period", ascending=True)
                .assign(
                    seller_id=lambda _: _["seller_id"],
                    meet_deadline=lambda _: where(_["period"] < 0, "Yes", "No"),
                    period=lambda _: round(_["period"], 2)
                )
                # 
                .head(top)
            )
            # The average days of the top n sellers
            avg_top_days = func_df["period"].mean()

            func_df = func_df.rename(
                columns={
                    "seller_id": "seller Id", 
                    "period": "Avg. Days before Deadline", 
                    "meet_deadline": "Meet Deadline"
                }
            )

            return {
                "error": False,
                "message": "",
                "data": func_df,
                "avg_days": avg_top_days
            }
