from dash import html
from dash_iconify import DashIconify 
import dash_mantine_components as dmc
from dash.exceptions import PreventUpdate
from pandas import read_json
from io import StringIO

from components.utils import delivery_phase, default_date_variable
from logic.duration_function import *
from logic.global_function import clean_date, filter_month




def valid_phase_options(from_phase_value: str, to_phase_value: str) -> tuple:
    """ 
    """
    if from_phase_value is not None and to_phase_value is not None:
        first_data = [data for data in delivery_phase if data != to_phase_value]
        second_data = [data for data in delivery_phase if data != from_phase_value]

        return (first_data, second_data)
    else:
        raise PreventUpdate


def update_bc_style(from_phase_value: str, to_phase_value: str) -> tuple:
    """ 
    """
    if from_phase_value is not None and to_phase_value is not None:
        output_tuple = ()
        for phase in delivery_phase:
            el_class = f"{'dp-bc_item'} active" if phase in [from_phase_value, to_phase_value] else "dp-bc_item"
            output_tuple = output_tuple + (el_class,)

        return output_tuple
    else:
        raise PreventUpdate


def store_date_diff_data(data_dict: dict, month: str, from_phase: str, to_phase: str, period) -> tuple:
    """ 
    """
    if data_dict != {}:        
        # Filter only the selected month
        flt_dict = filter_month(
            clean_date(DataFrame(data_dict), "orders"),
            default_date_variable,
            month,
            False, 
            True
        )
        
        if flt_dict["error"]:
            raise PreventUpdate
        else:
            phase_list = arrange_selection(from_phase, to_phase)
            # Create date difference for filtered month
            time_diff_dict = create_time_diff(
                flt_dict["data"],
                phase_list[0],
                phase_list[1],
                period
            )
            
            if time_diff_dict["error"]:
                raise PreventUpdate
            else:
                return (
                    flt_dict["data"].to_dict('records'),
                    time_diff_dict["data"].to_dict('records')
                )
    else:
        raise PreventUpdate


def update_ut_table(data_dict: dict) -> tuple:
    """ 
    """
    if data_dict != {}:
        ut_dict = unit_of_time(DataFrame(data_dict))

        if ut_dict["error"]["type"]:
            raise PreventUpdate
        else:
            count_tuple = ()
            percent_tuple = ()
            for idx in range(4):
                count_tuple = count_tuple + (f"{ut_dict['count'][idx]:,}", )
                percent_tuple = percent_tuple + (ut_dict['percentage'][idx], )

            all_output = count_tuple + percent_tuple
            return all_output
    else:
        raise PreventUpdate
    

def update_median_day_chart(diff_data_dict: dict, from_phase: str, to_phase: str, period: str) -> tuple:
    """ 
    """
    if diff_data_dict != {}:
        func_data = clean_date(DataFrame(diff_data_dict), "orders")
        phase_diff_cols = arrange_selection(from_phase, to_phase, labels=True)

        return median_duration_day(func_data, default_date_variable, phase_diff_cols, period)
    else:
        raise PreventUpdate


def update_median_month_chart(lu_data_dict: dict, month: str, from_phase: str, to_phase: str, period: str):
    """ 
    """
    if lu_data_dict != {}:
        # Filter the all months leading up to the selected month
        lu_flt_dict = filter_month(
            clean_date(DataFrame(lu_data_dict), "orders"),
            default_date_variable,
            month,
            True, 
            True
        )

        if lu_flt_dict["error"]:
            raise PreventUpdate
        else:
            phase_list = arrange_selection(from_phase, to_phase)
            # Create date difference for all available months
            lu_time_diff_dict = create_time_diff(
                lu_flt_dict["data"],
                phase_list[0],
                phase_list[1],
                period
            )

            if lu_time_diff_dict["error"]:
                raise PreventUpdate
            else:
                return median_duration_month(
                    lu_time_diff_dict["data"], 
                    default_date_variable, 
                    period,
                    month
                )
    else:
        raise PreventUpdate
    

def update_actual_estimated_chart(data_dict: dict, period: str):
    """ 
    """

    if data_dict != {}:

        return estimate_actual(clean_date(DataFrame(data_dict), "orders"), period)
    else:
        raise PreventUpdate