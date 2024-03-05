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
dash.register_page(__name__, path='/', name="Orders Insight", description="Product Order metrics for different months")


order_page_content_layout = html.Div(
    [
        dcc.Store(id="store_selected_month_data", data={}),
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
    Output("store_selected_month_data", "data"),

    Input('store_orders_data', 'data'),
    Input("orders_selected_month", "value")
)
def filter_selected_month(data, month):
    return filter_single_month(data, month)


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
    return update_count_stats(data, month, "orders")



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
    return update_count_stats(data, month, "customer")


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
    Input("store_selected_month_data", "data"),
    Input("orders_selected_month", "value")
)
def update_charts(data, single_month_data, month):
    return update_chart_callback(data, single_month_data, month)


@callback(
    Output("delivered_status", "children"),
    Output("shipped_status", "children"),
    Output("canceled_status", "children"),
    Output("unavailable_status", "children"),
    Output("invoiced_status", "children"),

    Input("store_selected_month_data", "data"),
    Input("orders_selected_month", "value")
)
def update_status_cat_count(data, month):
    return update_status_count(data, month)



# def toggle_modal(n_click, opened):
#     return not opened

# for status_model_id in delivery_status:
#     callback(
#         Output(f"{status_model_id}_modal", "opened"),
#         Input(f"{status_model_id}_trigger", "n_clicks"),
#         State(f"{status_model_id}_modal", "opened"),
#         prevent_initial_call=True
#     )(toggle_modal)


# Modal toggle

@callback(
    Output("delivered_modal", "opened"),
    Input("delivered_trigger", "n_clicks"),
    State("delivered_modal", "opened"),
    prevent_initial_call=True
)
def toggle_delivered_modal(n_click, opened):
    return not opened

@callback(
    Output("shipped_modal", "opened"),
    Input("shipped_trigger", "n_clicks"),
    State("shipped_modal", "opened"),
    prevent_initial_call=True
)
def toggle_shipped_modal(n_click, opened):
    return not opened

@callback(
    Output("canceled_modal", "opened"),
    Input("canceled_trigger", "n_clicks"),
    State("canceled_modal", "opened"),
    prevent_initial_call=True
)
def toggle_canceled_modal(n_click, opened):
    return not opened

@callback(
    Output("unavailable_modal", "opened"),
    Input("unavailable_trigger", "n_clicks"),
    State("unavailable_modal", "opened"),
    prevent_initial_call=True
)
def toggle_unavailable_modal(n_click, opened):
    return not opened

@callback(
    Output("invoiced_modal", "opened"),
    Input("invoiced_trigger", "n_clicks"),
    State("invoiced_modal", "opened"),
    prevent_initial_call=True
)
def toggle_invoiced_modal(n_click, opened):
    return not opened
    

@callback(
    Output("delivered_month_chart", "figure"),

    Input("delivered_modal", "opened"),
    Input('store_orders_data', 'data'),
    Input("orders_selected_month", "value"),
    prevent_initial_call=True
)
def update_delivered_chart(is_opened: bool, data: dict, month: str):
    return update_status_charts(data, month, is_opened, "delivered")

@callback(
    Output("shipped_month_chart", "figure"),

    Input("shipped_modal", "opened"),
    Input('store_orders_data', 'data'),
    Input("orders_selected_month", "value"),
    prevent_initial_call=True
)
def update_shipped_chart(is_opened: bool, data: dict, month: str):
    return update_status_charts(data, month, is_opened, "shipped")

@callback(
    Output("canceled_month_chart", "figure"),

    Input("canceled_modal", "opened"),
    Input('store_orders_data', 'data'),
    Input("orders_selected_month", "value"),
    prevent_initial_call=True
)
def update_canceled_chart(is_opened: bool, data: dict, month: str):
    return update_status_charts(data, month, is_opened, "canceled")

@callback(
    Output("unavailable_month_chart", "figure"),

    Input("unavailable_modal", "opened"),
    Input('store_orders_data', 'data'),
    Input("orders_selected_month", "value"),
    prevent_initial_call=True
)
def update_unavailable_chart(is_opened: bool, data: dict, month: str):
    return update_status_charts(data, month, is_opened, "unavailable")

@callback(
    Output("invoiced_month_chart", "figure"),

    Input("invoiced_modal", "opened"),
    Input('store_orders_data', 'data'),
    Input("orders_selected_month", "value"),
    prevent_initial_call=True
)
def update_invoiced_chart(is_opened: bool, data: dict, month: str):
    return update_status_charts(data, month, is_opened, "invoiced")