from pandas import DataFrame
from dash.exceptions import PreventUpdate
from dash_iconify import DashIconify 
from dash_mantine_components.theme import DEFAULT_COLORS

from logic.global_function import check_valid_month_name, filter_month, clean_date
from logic.order_function import *
from components.utils import month_abbrev, default_date_variable, default_color, delivery_status


def update_count_stats(data_dict: dict, month: str, output_type: str) -> tuple:
    """ 
    """
    if data_dict != {}:
        # Convert to pandas dataframe
        func_df = clean_date(DataFrame(data_dict), output_type)
        # Get stats numbers 
        stats_dict = get_stats_numbers(func_df, default_date_variable, month, output_type)
            
        # Check for error while getting the stats
        if stats_dict["error"]:
            raise PreventUpdate
        else:

            # Current month vs previous month change icon output
            if stats_dict["change_text"] == "increase":
                change_icon = DashIconify(icon="solar:round-alt-arrow-up-broken", color=default_color, height=20)
            elif stats_dict["change_text"] == "decrease":
                change_icon = DashIconify(
                    icon="solar:round-alt-arrow-down-broken", color=DEFAULT_COLORS["red"][8], height=20
                )
            else:
                change_icon = DashIconify(
                    icon="solar:round-alt-arrow-down-broken", color=DEFAULT_COLORS["gray"][7], height=20
                ) # /!\ =====

            # Percentage change sectionf
            total_change_label = f"{stats_dict['percentage_total']}%"
            section = [{
                "value": stats_dict["percentage_total"], "color": default_color, "tooltip": total_change_label
            }]

            return (
                f"{stats_dict['volume']:,}",
                # stats_dict["prev_volume"],
                round(stats_dict["percentage_change"]),
                total_change_label,
                change_icon,
                section,
            )
    else:
        raise PreventUpdate


def update_months_values(data_dict: dict, month: str) -> tuple:
    """ 
    """
    if data_dict != {}:
        # Convert to pandas dataframe
        func_df = clean_date(DataFrame(data_dict), "orders")

        month_dict = month_stats(func_df, default_date_variable, month)

        # Check for error while getting the stats
        if month_dict["error"]:
            raise PreventUpdate
        else:
            month_range = f"Jan - {month_abbrev[month]}"
            mom_change = month_dict["MoM_change"]

            if mom_change > 0:
                mom_icon = DashIconify(icon="gg:arrow-up-o", color=default_color, height=20)
            elif mom_change < 0:
                mom_icon = DashIconify(icon="gg:arrow-drown-o", color=default_color, height=20)
            else:
                mom_icon = DashIconify(icon="bi:dash-circle", color=default_color, height=20)

            return (
                f"{month_dict['MTD']:,}",
                month_range,
                round(mom_change),
                month_dict["MoM_growth_rate"],
                mom_icon
            )

    else:
        raise PreventUpdate


def update_chart_callback(data_dict: dict, month: str):
    """ 
    """

    if data_dict != {}:
        # Convert to pandas dataframe
        func_df = clean_date(DataFrame(data_dict), "orders")

        # Filter selected month data
        data_dict = filter_month(func_df, default_date_variable, month, False, True)

        return (
            monthly_order_volume(func_df, default_date_variable, month, "line"),
            get_week_volume(data_dict, default_date_variable, month),
            daily_order_volume(data_dict, default_date_variable, month)
        )
    else:
        raise PreventUpdate


def update_status_count(data_dict: dict, month: str):
    """ 
    """ 

    if data_dict != {}:
        # Convert to pandas dataframe
        func_df = clean_date(DataFrame(data_dict), "orders")

        # Get the number of orders that fall within each status.
        status_dict = status_count(func_df, default_date_variable, month)
        # Check that status_dict is not an empty dictionary
        if status_dict != {}:
            output_tuple = ()
            for status in delivery_status:
                output_tuple += (f"{status_dict[status]:,}", )

            return output_tuple 
        else:
            raise PreventUpdate
    else:
        raise PreventUpdate
    

def update_status_chart(data_dict: dict, month: str, status_type: str):
    """ 
    """

    if data_dict != {}:
        if status_type in delivery_status:
            # Convert to pandas dataframe
            func_df = clean_date(DataFrame(data_dict), "orders")
            
            func_df = func_df.query(f"order_status == '{status_type}'")
            return monthly_order_volume(func_df, default_date_variable, month)
        else:
            raise PreventUpdate
    else:
        raise PreventUpdate
