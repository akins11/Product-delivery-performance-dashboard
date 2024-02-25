import dash
from dash import html, dcc
from dash import callback, Input, Output, State
import dash_mantine_components as dmc

from components.page_layout import dashboard_page_layout, graph_container, grid_container, grid_col
from components.stats_card import stats_card, mtd_card, mom_card
from components.utils import delivery_status
from components.order_comp import status_summary
from components.orders_callback import *

# Register page
dash.register_page(__name__, path='/', name="Orders Insight", description="Orders ...")


order_page_content_layout = html.Div(
    [
        html.Div(
            [
                stats_card("orders"),
                stats_card("customer"),
                mtd_card(),
                mom_card()
            ],
            className="ord-stats"
        ),

        grid_container(
            [
                grid_col(graph_container("order_month_chart"), span=8),
                grid_col(graph_container("order_weekend_weekday_chart"), span=4),
            ]
        ),
        
        grid_container(
            [
                grid_col(graph_container("order_days_chart"), span=8),
                grid_col(status_summary(), span=4),
            ]
        ),
    ],
    className="pmc-content"
)


layout = dashboard_page_layout(
    page_name_id = "orders",
    page_title = "Product Orders",
    page_content = order_page_content_layout
)



@callback(
    Output('orders_sidebar', 'className'),
    Input('orders_open_burger', 'opened')
)
def toggle_sidebar(is_opened):

    return "page-sidebar" if is_opened else "page-sidebar close"



@callback(
    Output("orders_count_value", "children"),
    Output("orders_percent_change", "children"),
    Output("orders_percent_text", "children"),
    Output("orders_change_icon", "children"),
    Output("orders_percent_chart_value", "sections"),

    Input('store_orders_data', 'data'),
    Input("orders_selected_month", "value")
)
def update_orders_count_stats(data, month):
    return update_count_stats(data_dict=data, month=month, output_type="orders")



@callback(
    Output("customer_count_value", "children"),
    Output("customer_percent_change", "children"),
    Output("customer_percent_text", "children"),
    Output("customer_change_icon", "children"),
    Output("customer_percent_chart_value", "sections"),

    Input('store_customer_data', 'data'),
    Input("orders_selected_month", "value")
)
def update_orders_count_stats(data, month):
    return update_count_stats(data_dict=data, month=month, output_type="customer")


@callback(
    Output("order_mtd", "children"),
    Output("order_mtd_month_abbr_name_range", "children"),
    Output("order_mom", "children"),
    Output("order_mom_growth_rate", "children"),
    Output("mom_icon_type", "children"),

    Input('store_orders_data', 'data'),
    Input("orders_selected_month", "value")
)
def update_month_stats(data, month):
    return update_months_values(data, month)


@callback(
    Output("order_month_chart", "figure"),
    Output("order_weekend_weekday_chart", "figure"),
    Output("order_days_chart", "figure"),

    Input('store_orders_data', 'data'),
    Input("orders_selected_month", "value")
)
def update_charts(data, month):
    return update_chart_callback(data, month)


@callback(
    Output("delivered_status", "children"),
    Output("shipped_status", "children"),
    Output("canceled_status", "children"),
    Output("unavailable_status", "children"),
    Output("invoiced_status", "children"),

    Input('store_orders_data', 'data'),
    Input("orders_selected_month", "value")
)
def update_status_cat_count(data, month):
    return update_status_count(data, month)



def toggle_modal(n_click, opened):
    return not opened

for status_model_id in delivery_status:
    callback(
        Output(f"{status_model_id}_modal", "opened"),
        Input(f"{status_model_id}_trigger", "n_clicks"),
        State(f"{status_model_id}_modal", "opened"),
        prevent_initial_call=True
    )(toggle_modal)


    
# @callback(
#     Output("delivered_month_chart", "figure"),

#     Input("delivered_modal", "opened"),
#     Input('store_orders_data', 'data'),
#     Input("orders_selected_month", "value")
# )
# def update_delivered_chart(is_opened: bool, data: dict, month: str):
#     if is_opened:
#         return update_status_chart(data, month, "delivered")
#     else:
#         raise PreventUpdate

# @callback(
#     Output("shipped_month_chart", "figure"),

#     Input("shipped_modal", "opened"),
#     Input('store_orders_data', 'data'),
#     Input("orders_selected_month", "value")
# )
# def update_shipped_chart(is_opened: bool, data: dict, month: str):
#     if is_opened:
#         return update_status_chart(data, month, "shipped")
#     else:
#         raise PreventUpdate

# @callback(
#     Output("canceled_month_chart", "figure"),

#     Input("canceled_modal", "opened"),
#     Input('store_orders_data', 'data'),
#     Input("orders_selected_month", "value")
# )
# def update_canceled_chart(is_opened: bool, data: dict, month: str):
#     if is_opened: 
#         return update_status_chart(data, month, "canceled")
#     else:
#         raise PreventUpdate

# @callback(
#     Output("unavailable_month_chart", "figure"),

#     Input("unavailable_modal", "opened"),
#     Input('store_orders_data', 'data'),
#     Input("orders_selected_month", "value")
# )
# def update_unavailable_chart(is_opened: bool, data: dict, month: str):
#     if is_opened: 
#         return update_status_chart(data, month, "unavailable")
#     else:
#         raise PreventUpdate

# @callback(
#     Output("invoiced_month_chart", "figure"),

#     Input('store_orders_data', 'data'),
#     Input("orders_selected_month", "value")
# )
# def update_invoiced_chart(data: dict, month: str):
#     return update_status_chart(data, month, "invoiced")