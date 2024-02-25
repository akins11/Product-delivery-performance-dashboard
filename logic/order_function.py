from pandas import DataFrame, Categorical
from numpy import where
import calendar
import plotly.express as px
from plotly.express import bar, line, pie
import plotly.io as pio

pio.templates.default = "plotly_white"

from logic.global_function import filter_month
from components.utils import default_color

plot_color = "#38D9A9"


def get_stats_numbers(df: DataFrame, date_var: str, month_name: str, output_type: str) -> dict:
    """
    :params
    df: App data.
    month_name: input month name.
    output_type: either ['order_volume', 'unique_customers']

    :return a dictionary of Order volume values.
    """
    # reusable error dictionary.
    error_dict =  {
        "error": True,
        "message": " ",
        "volume": None,
        "prev_volume": None,
        "percentage_change": None,
        "change_text": None,
        "percentage_total": None
    }
    
    # check if output type is accurately described.
    if output_type not in ["orders", "customer"]:
        error_dict["message"] = "Invalid `output_type` value. Please input either 'order_volume' or 'unique_customers'"
        return error_dict
    
    # Get the list of month name and assign them their respective ids
    month_list = list(calendar.month_name[1:])
    month_dic = {month_list[i] : i+1 for i in range(len(month_list))}
    # Get previous month name 
    if month_name != "January":
        previous_month_dict = {name: value for name, value in month_dic.items() if value == month_dic[month_name]-1}
    else:
        previous_month_dict = {"December": 12}
    previous_month_name = [name for name in previous_month_dict.keys()][0]
    
    try:
        # Get all the rows of for the total orders leading up to the input month, the current month and
        # previous month.
        total_month_df = filter_month(df, date_var, month_name, True)["data"]
        current_month_df = filter_month(df, date_var, month_name, False)["data"]
        previous_month_df = filter_month(df, date_var, previous_month_name, False)["data"]

        if output_type == "orders":
            total_month = total_month_df.shape[0]
            current_month = current_month_df.shape[0]
            previous_month = previous_month_df.shape[0]
        else:
            total_month = total_month_df["customer_unique_id"].nunique()
            current_month = current_month_df["customer_unique_id"].nunique()
            previous_month = previous_month_df["customer_unique_id"].nunique()

        percentage_total = int((current_month / total_month)*100)

        change = round((current_month - previous_month) / previous_month * 100, 2)
        if change > 0:
            change_text = "increase"
        elif change == 0:
            change_text = "stable"
        else:
            change_text = "decrease"

        return {
            "error": False,
            "message": "",
            "volume": current_month,
            "prev_volume": previous_month,
            "percentage_change": change,
            "change_text": change_text,
            "percentage_total": percentage_total
        }
    except ValueError as e:
        error_dict["message"] = f"An error occured while summarising order volume: {e}"
        return error_dict


def month_stats(df: DataFrame, date_var: str, month_name: str) -> dict:
    """
    :params
    df: App data.
    date_var: a date variable from the df, used to filter the data.
    month_name: input month (dashboard current month).

    :return a dictionary containing The MTD and MoM values.
    """

    try:
        # Month to Date
        MTD = filter_month(df, date_var, month_name, True, True)["data"].shape[0]

        # Month over Month
        # Get the list of month name and assign them their respective ids
        month_list = list(calendar.month_name[1:])
        month_dic = {month_list[i] : i+1 for i in range(len(month_list))}
        # Get previous month name 
        if month_name != "January":
            previous_month_dict = {name: value for name, value in month_dic.items() if value == month_dic[month_name]-1}
        else:
            previous_month_dict = {"December": 12}
        previous_month_name = [name for name in previous_month_dict.keys()][0]

        # get the input month and the previous month order volume.
        month_current_value = filter_month(df, date_var, month_name, False, True)["data"].shape[0]
        month_previous_value = filter_month(df, date_var, previous_month_name, False, False)["data"].shape[0]
        # Calculate the percentage change of the input month against the prevous month.
        MoM_change = (month_current_value - month_previous_value) / month_previous_value * 100
        # Calculate the growth rate of the input month against the previous month
        MoM_growth = (month_current_value - month_previous_value) - 1

        return {
            "error": False,
            "message": " ",
            "MTD": MTD,
            "MoM_change": MoM_change,
            "MoM_growth_rate": MoM_growth
        }
    except ValueError as e:
        return {
            "error": True,
            "message": f"An error occured while calculating month stats: {e}",
            "MTD": None,
            "MoM_change": None,
            "MoM_growth_rate": None
        }


def monthly_order_volume(df: DataFrame, date_var: str, month_name: str, plot_type: str="line"):
    """
    :params
    df: App data
    date_var: a date variable from the df, used to filter the data.
    month_name: input month (dashboard current month).
    plot_type: the type of plot to return either a 'line' or 'bar' chart

    :return a plotly object. 
    """

    # Filter input month and other previous month
    data_dict = filter_month(df, date_var, month_name, True, True)

    if data_dict["error"] != True:
        month_names = data_dict["data"][date_var].dt.strftime("%B").unique()
        month_cat = [name for name in list(calendar.month_name[1:]) if name in month_names]
        
        plt_df = (
            data_dict["data"]
            .assign(month=lambda _: _[date_var].dt.strftime("%B"))
            ["month"].value_counts(sort=False)
            .reset_index().reset_index() # /!\ Double /!\
            .assign(month=lambda _: Categorical(_["month"], categories=month_cat, ordered=True))
            .sort_values(by="month")
        )

        plt_title = f"Order Volume Performance Up to {month_name}"
        plt_labs = {"month": " ", "count": "Orders"}

        if plot_type == "bar":
            func_fig = bar(
                data_frame=plt_df, 
                x="month", y="count",
                title=plt_title, labels=plt_labs,
                color_discrete_sequence=[plot_color]
            )
            marker_dict = {}
        else:
            func_fig = line(
                data_frame=plt_df, 
                x="month", y="count",
                markers=True,
                title=plt_title, labels=plt_labs,
                color_discrete_sequence=[plot_color]
            )
            marker_dict = dict(
                size=12,
                color="#FFFFFF",
                line=dict(width=2, color=plot_color)
            )

        func_fig.update_traces( 
            marker=marker_dict,
            hovertemplate="<b>%{x}</b><br><b>Volume: %{y:,}</b>",
            hoverlabel=dict(
                bgcolor="#FFFFFF",
                font_size=16,
                font=dict(color=plot_color),
                bordercolor=plot_color
            )
        )

        func_fig.update_xaxes(showgrid=False, tickmode="linear", dtick=1)
        return func_fig
    else:
        return px.line()


def daily_order_volume(df: DataFrame, date_var: str, month_name: str):
    """
    :params
    df: App data.
    date_var: a date variable from the df, used to filter the data.
    month_name: input month (dashboard current month).

    :return a plotly object
    """

    data_dict = filter_month(df, date_var, month_name, False, True)

    if data_dict["error"] == False:
        func_df = (
            data_dict["data"]
            .assign(day=lambda _: _[date_var].dt.day)
            ["day"]
            .value_counts()
            .reset_index()
            .sort_values(by="day")
        )

        func_fig = line(
            data_frame=func_df,
            x="day", y="count",
            markers=True,
            labels={"day": "Days", "count": "Orders"},
            title = f"Order Volume for the Month of {month_name}",
            color_discrete_sequence=[plot_color]
        )

        func_fig.update_traces( 
            marker=dict(
                size=5,
                color="#FFFFFF",
                line=dict(width=2, color=plot_color)
            ),
            hovertemplate="<b>Day - %{x}</b><br><b>Volume: %{y:,}</b>",
            hoverlabel=dict(
                bgcolor="#FFFFFF",
                font_size=16,
                font=dict(color=plot_color),
                bordercolor=plot_color
            )
        )
        # func_fig.update_layout(height=400)
        func_fig.update_xaxes(showgrid=False) #tickmode="linear", dtick=1
        return func_fig
    else:
        return line()


def get_week_volume(df: DataFrame, date_var: str, month_name: str):
    """ 
    :params
    df: App data.
    date_var: a date variable from the df, used to filter the data.
    month_name: input month (dashboard current month).

    :return a plotly object
    """

    data_dict = filter_month(df, date_var, month_name, False, True)

    if data_dict["error"] == False:
        func_df = (
            data_dict["data"]
            .assign(
                day_of_week=lambda _: _[date_var].dt.dayofweek,
                week_period=lambda _: where((_["day_of_week"] >= 0) & (_["day_of_week"] <= 4), "Weekday", "weekend")
            )["week_period"]
            .value_counts().reset_index()
        )

        func_fig = pie(
            data_frame=func_df,
            names="week_period",
            values="count",
            hole=0.5,
            title="Order Volume by Weekdays & Weekends",
            color_discrete_sequence=["#087F5B", "#96F2D7"]
        )

        func_fig.update_traces(
            textposition='none',
            hovertemplate="<b>%{label}</b><br><b>Volume: %{value:,}</b><br>%{percent:.2f}%", ## /!\/!\
            hoverlabel=dict(font_size=16)
        )
        return func_fig
    else:
        return pie()
    


def status_count(df: DataFrame, date_var: str, month_name: str) -> dict:
    """
    :params
    df: App data.
    date_var: a date variable from the df, used to filter the data.
    month_name: input month (dashboard current month).

    :return a dictionary of status count for the inputed month.
    """

    # info
    # if a particular status is missing in a month, replace them with zero

    data_dict = filter_month(df, date_var, month_name, False, True)

    if data_dict["error"] == False:
        return data_dict["data"]["order_status"].value_counts().to_dict()
    else:
        return {}
    































































    