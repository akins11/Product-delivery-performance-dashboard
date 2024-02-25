from pandas import DataFrame, Timedelta, Categorical
from numpy import where
import calendar
from plotly.express import line, bar, colors
import plotly.io as pio

pio.templates.default = "plotly_white"

from components.utils import default_color

plot_color = "#38D9A9"


 
def arrange_selection(first_date: str, second_date: str, labels: bool=False) -> list:
    """ 
    :params
    first_date: Inputed frist date.  
    second_date: Inputed second date.

    :return a list of arranged date column name. 
    """
    # Original date column names
    col_dict = {
        "placement": "order_purchase_timestamp",
        "approval": "order_approved_at",
        "carrier": "order_delivered_carrier_date",
        "customer": "order_delivered_customer_date"
    }
    # arranged inputes
    arranged_dict = {
        "customer_placement": ["placement", "customer"],
        "approval_placement": ["placement", "approval"],
        "carrier_placement":  ["placement", "carrier"],
        "approval_carrier":   ["approval", "carrier"],
        "approval_customer":  ["approval", "customer"],
        "carrier_customer":   ["carrier", "customer"]
    }
    # Sort the values in alphabetical order.
    alpha_sorting = sorted([first_date, second_date])
    # combine sorted value to create a valid key
    request = "_".join(alpha_sorting)

    if labels:
        return [str.title(lab) for lab in arranged_dict[request]]
    else:
        return [col_dict[arranged_dict[request][0]], col_dict[arranged_dict[request][1]]]


def create_time_diff(data: DataFrame, first_date: str, second_date: str, num_unit: str="minute") -> dict:
    """ 
    :params
    data: App data.
    first_date: a date column name corresponding to the latest date.
    second_date: a date column name corresponding to the past date.
    num_unit: The unit of time the difference should be measured.

    :return a pandas dataframe.
    """

    # Make a copy of the supplied data
    func_df = data.copy()

    try:
        # Add the time difference column (second date [current] - first date [current])
        func_df["time_diff"] = (func_df[second_date] - func_df[first_date])

        # Add the days, hours, minutes and seconds date components
        date_components = ["days", "hours", "minutes", "seconds"]
        func_df[date_components] = func_df["time_diff"].dt.components[date_components]

        # Add date component label
        func_df["unit_time"] = where(
            func_df["days"] > 0, "Days", where(
                func_df["hours"] > 0, "Hours", where(
                    func_df["minutes"] > 0, "Minutes", "Seconds"
                )
            )
        )

        # Add Numeric unit
        if num_unit == "second":
            func_df["period"] = func_df["time_diff"] / Timedelta(seconds=1)
        elif num_unit == "minute":
            func_df["period"] = func_df["time_diff"] / Timedelta(minutes=1)
        elif num_unit == "hour":
            func_df["period"]   = func_df["time_diff"] / Timedelta(hours=1)
        elif num_unit == "day":
            func_df["period"]    = func_df["time_diff"] / Timedelta(days=1)
        else:
            func_df["period"]   = func_df["time_diff"] / Timedelta(weeks=1)

        return {"error": False, "message": "", "data": func_df}
    
    except ValueError as e:
        return {
            "error": True, 
            "message": f"An error occured while trying to get the date diff: {e}", 
            "data": None
        }

    
def unit_of_time(data: DataFrame) -> dict:
    """ 
    :param
    data: App data with a date difference applied to the data.

    :return a dictionary with the summarised count and percentage of each unit of time. 
    """

    try:
        unit_time_lab = ["Seconds", "Minutes", "Hours", "Days"]

        func_dict = (
            data["unit_time"]
            .value_counts()
            .reset_index()
            .assign(percentage=lambda _: round(_["count"] / _["count"].sum() * 100, 1))
            .to_dict()
        )
        # Check if all unit time are available
        if len(func_dict["unit_time"]) != 4:
            # Collect available unit time labels 
            av_values = list(func_dict["unit_time"].values()) 
            # Collect all missing values
            miss_values = [v for v in unit_time_lab if v not in av_values]
            # Get the number of values
            len_idx = len(func_dict["unit_time"])
            for i in miss_values:
                func_dict["unit_time"][len_idx] = i
                func_dict["count"][len_idx] = 0
                func_dict["percentage"][len_idx] = 0
                len_idx += 1

            func_dict = (
                DataFrame(func_dict)
                .assign(unit_time=lambda _: _['unit_time'].astype("category"))
                .assign(unit_time=lambda _: _['unit_time'].cat.reorder_categories(unit_time_lab, ordered=True))
                .sort_values(by="unit_time")
                .reset_index(drop=True)
                .to_dict()
            )

        func_dict["error"] = {"type": False, "message": ""}

        return func_dict
    
    except ValueError as e:
        return {"unit_time": {}, "count": {}, "percentage": {}, "error": {"type": True, "message": e}}


def median_duration_day(data: DataFrame, date_var: str, diff_cols: list[str], period: str):
    """
    :params
    data: App data with a date difference applied to the data.
    date_var: The name of the date column to extract the unique days (order_purchase_timestamp).
    diff_cols: a list of the two differenced date columns label.
    
    :retrun a plotly object.
    """

    # Create a copy of the data
    func_df = data.copy()
    # Summarise the duration using the median aggregate function for each days in the inputed month.
    func_df = (
        func_df
        .assign(day=lambda _: _[date_var].dt.day)
        .groupby("day")["period"].median()
        .reset_index()
    )

    # print(func_df)

    # Plot the result
    fun_fig = bar(
        data_frame=func_df,
        x="day", y="period",
        labels={"period": f"Period: {str.title(period)}s", "day": "Day"},
        title=f"Median Duration from {diff_cols[0]} to {diff_cols[1]}",
        color_discrete_sequence=[plot_color]
    )

    fun_fig.update_traces(
        hovertemplate = f"<b>Day - %{{x}} </b><br><b>{str.title(period)}s: %{{y:,.2f}} </b>",
        hoverlabel=dict(
            bgcolor="#FFFFFF",
            font_size=18,
            font=dict(color=plot_color),
            bordercolor=plot_color
        )
    )

    fun_fig.update_xaxes(showgrid=False) #, tickmode="linear", dtick=1

    return fun_fig


def median_duration_month(data: DataFrame, date_var: str, period: str, month: str):
    """
    :params
    data: App data with a date difference applied to the data.
    date_var: The name of the date column to extract the unique days (order_purchase_timestamp).
    month: Name of the input month.

    :return a plotly object.
    """
    # Copy data
    func_df = data.copy()

    # Get the available ordered month name
    month_names = func_df[date_var].dt.strftime("%b").unique()
    month_cat = [name for name in list(calendar.month_abbr[1:]) if name in month_names] 
    # Summarise the duration using the median aggregate function for each month leading to the inputed month.
    func_df = (
        func_df
        .assign(month=lambda _: _[date_var].dt.strftime("%b"))
        .groupby("month")["period"].median()
        .reset_index()
        .assign(month=lambda _: Categorical(_["month"], categories=month_cat, ordered=True))
        .sort_values(by="month")
    )

    # Plot the result
    func_fig = line(
        data_frame=func_df, 
        x="month", y="period",
        markers=True,
        labels={"period": f"{str.title(period)}s", "month": "Month"},
        title=f"Median Duration Up to {month}",
        color_discrete_sequence=[plot_color]
    )

    func_fig.update_traces(
        marker=dict(
            size=12,
            color="#FFFFFF",
            line=dict(width=2, color=plot_color)
        ),
        hovertemplate=f"<b>%{{x}} </b><br><b>{str.title(period)}s: %{{y:,.2f}} </b>",
        hoverlabel=dict(
            bgcolor="#FFFFFF",
            font_size=18,
            font=dict(color=plot_color),
            bordercolor=plot_color
        )
    )
    return func_fig


def get_min_max_duration(data: DataFrame) -> dict:
    """
    :param
    data: App data with a date difference applied to the data.

    :return a dictionary
    """

    try:
        min_td = data["time_diff"].min()
        max_td = data["time_diff"].max()

        def components(time_delta) -> list:
            days = time_delta.days
            hours = time_delta.seconds // 3600
            minutes = (time_delta.seconds % 3600) // 60
            seconds = time_delta.seconds % 60

            return [days, hours, minutes, seconds]

        component_names = ["days", "hours", "minutes", "seconds"]
        min_duration = {comp: value for comp, value in zip(component_names, components(min_td))}
        max_duration = {comp: value for comp, value in zip(component_names, components(max_td))}

        def format_duration(duration: dict) -> str:

            days = f"{duration['days']} day(s)" if duration["days"] != 0 else ""
            hrs = f"{duration['hours']} hour(s)" if duration["hours"] != 0 else ""
            min = f"{duration['minutes']} minute(s)" if duration["minutes"] != 0 else ""

            return str.strip(f"{days} {hrs} {min} {duration['seconds']} seconds")
        
        return {
            "error": False, "message": "", 
            "min_duration": format_duration(min_duration),
            "max_duration": format_duration(max_duration),
            "min_duration_dict": min_duration,
            "max_duration_dict": max_duration
        }
    
    except ValueError as e:
        return {
            "error": True, "message": f"An error occured while trying to extract the min/max duration: {e}", 
            "min_duration": None, "max_duration": None,
            "min_duration_dict": None, "max_duration_dict": None
        }


def estimate_actual(data: DataFrame, num_unit: str="day"):
    """
    :params
    data: App (Filterd) data.
    num_unit: The unit of time the difference should be measured.

    :return a plotly object.
    """

    # Make a copy of the supplied data
    func_df = data.copy()

    func_df["actual_time_diff"] = (func_df["order_delivered_customer_date"] - func_df["order_purchase_timestamp"])
    func_df["estimate_time_diff"] = (func_df["order_delivered_customer_date"] - func_df["order_estimated_delivery_date"])

    for i in ["actual", "estimate"]:
        if num_unit == "second":
            func_df[f"{i}_period"] = func_df[f"{i}_time_diff"] / Timedelta(seconds=1)
        elif num_unit == "minute":
            func_df[f"{i}_period"] = func_df[f"{i}_time_diff"] / Timedelta(minutes=1)
        elif num_unit == "hour":
            func_df[f"{i}_period"] = func_df[f"{i}_time_diff"] / Timedelta(hours=1)
        elif num_unit == "day":
            func_df[f"{i}_period"] = func_df[f"{i}_time_diff"] / Timedelta(days=1)
        else:
            func_df[f"{i}_period"] = func_df[f"{i}_time_diff"] / Timedelta(weeks=1)

    # Summarise duration for each day of the input month.
    func_df = (
        func_df
        .assign(day=lambda _: _["order_purchase_timestamp"].dt.day)
        .groupby("day")
        .agg(
            Estimated=("estimate_period", "median"),
            Actual   =("actual_period", "median")
        )
        .reset_index()
        .assign(Estimated=lambda _: abs(_["Estimated"]))
        .melt(id_vars="day", var_name="type", value_name=f"median_{num_unit}")
    )
    
    # Plot output
    func_fig = line(
        data_frame=func_df,
        x="day", y=f"median_{num_unit}", color="type",
        custom_data=["type"],
        title="Median Delivery Duration (Extimate vs Actual)",
        labels={f"median_{num_unit}": f"{str.title(num_unit)}s", "day": "Days"},
        color_discrete_sequence=["#087F5B", "#96F2D7"]
    )

    func_fig.update_traces(
        hovertemplate = "<b>%{customdata[0]}</b><br><b>Day: %{x}</b><br><b>Median: %{y:,.1f}</b><extra></extra>",
        hoverlabel=dict(font_size=18)
    )

    func_fig.update_xaxes(showgrid=False) # ,tickmode="linear", dtick=1

    return func_fig

























