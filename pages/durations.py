import dash
from dash import html, dcc
import dash_mantine_components as dmc
from dash import callback, Input, Output
from dash.exceptions import PreventUpdate

from components.page_layout import dashboard_page_layout, grid_container, grid_col
from components.duration_comp import * 
from components.utils import config_plotly, delivery_phase
from components.duration_callback import *

# Register page
dash.register_page(__name__, name="Order Shipping Duration", description="Duration of shipping product ..")

duration_page_content_layout = html.Div(
    [
        dcc.Store(id=f"month_filtered_data", data={}),
        dcc.Store(id=f"date_diff_data", data={}),

        
        grid_container(
            [
                grid_col(breadcrumb(), span=8),
                grid_col(phase_selection(), span=4)
            ]
        ),

        grid_container(
            [
                grid_col(unit_of_time_table(), span=6),
                grid_col(figure_output_ui("duration_median_day", "day"), span=6),
            ]
        ),
        
        grid_container(
            [
                grid_col(figure_output_ui("duration_median_month"), span=6),
                grid_col(figure_output_ui("duration_estimated_actual"), span=6),
            ]
        ),
    ],
    className="pmc-content"
)


layout = dashboard_page_layout(
    page_name_id = "duration",
    page_title = "Delivery Duration",
    page_content = duration_page_content_layout
)



@callback(
    Output('duration_sidebar', 'className'),
    Input('duration_open_burger', 'opened')
)
def toggle_sidebar(is_opened):
    return "page-sidebar" if is_opened else "page-sidebar close"


@callback(
    Output("from_phase", "data"),
    Output("to_phase", "data"),

    Input("from_phase", "value"),
    Input("to_phase", "value"),
    prevent_initial_call=True
)
def update_delivery_phase_data(from_phase, to_phase):
    return valid_phase_options(from_phase, to_phase)
# suppress_callback_exceptions=True

@callback(
    Output("placement", "className"),
    Output("approval", "className"),
    Output("carrier", "className"),
    Output("customer", "className"),

    Input("from_phase", "value"),
    Input("to_phase", "value")
)
def update_bc_phase(from_phase, to_phase):
    return update_bc_style(from_phase, to_phase)


@callback(
    Output("month_filtered_data", "data"),
    Output("date_diff_data", "data"),

    Input('store_orders_data', 'data'),
    Input("duration_selected_month", "value"),
    Input("from_phase", "value"),
    Input("to_phase", "value"),
    Input('duration_median_day_period', 'value')
)
def create_date_difference(data, month, from_phase, to_phase, period):
    return store_date_diff_data(data, month, from_phase, to_phase, period)


@callback(
    Output("second_count", "children"),
    Output("minute_count", "children"),
    Output("hour_count", "children"),
    Output("day_count", "children"),

    Output("second_percent", "children"),
    Output("minute_percent", "children"),
    Output("hour_percent", "children"),
    Output("day_percent", "children"),

    Input("date_diff_data", "data"),
)
def update_unit_time_table_values(data):
    return update_ut_table(data)

@callback(
    Output("duration_median_day", "figure"),

    Input("date_diff_data", "data"),
    # Input("orders_selected_month", "value")
    Input("from_phase", "value"),
    Input("to_phase", "value"),
    Input('duration_median_day_period', 'value')
)
def update_day_charts(diff_data, from_phase, to_phase, period):
    return update_median_day_chart(diff_data, from_phase, to_phase, period)


@callback(
    Output("duration_median_month", "figure"),
    Input('store_orders_data', 'data'),
    Input("duration_selected_month", "value"),
    Input("from_phase", "value"),
    Input("to_phase", "value"),
    Input('duration_median_month_period', 'value'),
)
def update_month_chart(lu_data, month, from_phase, to_phase, period):
    return update_median_month_chart(lu_data, month, from_phase, to_phase, period)


@callback(
    Output("duration_estimated_actual", "figure"),
    Input('month_filtered_data', 'data'),
    Input('duration_estimated_actual_period', 'value'),
)
def update_actual_vs_estimated_chart(data, period):
    return update_actual_estimated_chart(data, period)