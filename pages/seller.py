import dash
from dash import html, dash_table
from dash import callback, Input, Output
from dash.exceptions import PreventUpdate
import dash_mantine_components as dmc
from pandas import DataFrame
from dash_mantine_components.theme import DEFAULT_COLORS

from components.page_layout import dashboard_page_layout, grid_container, grid_col
from components.stats_card import seller_stats_card
from components.utils import default_date_variable, default_color

from logic.seller_function import seller_count, top_sellers_order_deadline
from logic.global_function import clean_date


default_column_names = ["seller_id", "Avg. Days Before Deadline", "Meet Deadline"]


# Register page
dash.register_page(__name__, name="Seller Peformance", description="summary of sellers activities")



seller_page_content_layout = html.Div(
    [

        grid_container(
            [
                grid_col(seller_stats_card(), span=5),
                grid_col(
                    [
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.Div(
                                            [
                                                dmc.Text("Top 5"),
                                                dmc.NumberInput(
                                                    label="",
                                                    value=5,
                                                    min=5, max=100,
                                                    step=5,
                                                    id="top_n_seller",
                                                    style={"width": "200px"}
                                                )
                                            ],
                                            className="sp-top_settings"
                                        ),

                                        html.Div(
                                            [
                                                dmc.Text("Average Days:", color=default_color),
                                                dmc.Text("0000", id="avg_day_duration")
                                            ],
                                            className="sp-avg_container"
                                        )
                                    ],
                                    className="sp-top_content"
                                ),

                                html.Div(
                                    [
                                        dash_table.DataTable(
                                            id="top_seller_deadline_table",
                                            columns=[{"name": i, "id": i} for i in default_column_names],
                                            style_as_list_view=True,
                                            style_header={
                                                "backgroundColor": default_color,
                                                "color": "#FFFFFF",
                                                "fontWeight": "bold",
                                                "border": "1px solid #FFFFFF",
                                            }
                                        )
                                    ],
                                    className="sp-top_table",
                                    id="top_seller_deadline"
                                )
                            ],
                            className="sp-top_container"
                        )
                    ],
                    span=7
                )
            ]
        ),
    ],
    className="pmc-content"
)

layout = dashboard_page_layout(
    page_name_id = "seller",
    page_title = "Sellers Performance",
    page_content = seller_page_content_layout
)



@callback(
    Output('seller_sidebar', 'className'),
    Input('seller_open_burger', 'opened')
)
def toggle_sidebar(is_opened):
    return "page-sidebar" if is_opened else "page-sidebar close"


@callback(
    Output("seller_count", "children"),
    Output("total_seller_count", "children"),
    Output("seller_percentage_chart", "sections"),
    Output("seller_percent_text_value", "children"),

    Input("store_seller_data", "data"),
    Input("seller_selected_month", "value")
)
def update_seller_count(data, month):
    
    if data != {}:
        func_data = clean_date(DataFrame(data), "seller")
        count_dict = seller_count(func_data, default_date_variable, month)

        if count_dict["error"]:
            raise PreventUpdate
        else:
            chart_section = [{"value": count_dict["percentage"], "color": default_color}]

            return (
                f"{count_dict['seller_count']:,}",
                f"{count_dict['overall_seller_count']:,}",
                chart_section,
                f"{count_dict['percentage']}%"
            )
    else:
        raise PreventUpdate
    


@callback(
    Output("top_seller_deadline", "children"),
    Output("avg_day_duration", "children"),

    Input("store_seller_data", "data"),
    Input("seller_selected_month", "value"),
    Input("top_n_seller", "value")
)
def update_top_table(data, month, top_n):
    """ 
    """
    if data != {}:
        func_data = clean_date(DataFrame(data), "seller")
        top_dict = top_sellers_order_deadline(func_data, default_date_variable, month, top_n)

        if top_dict["error"]:
            raise PreventUpdate
        else:
            table =  dash_table.DataTable(
                id="top_seller_deadline_table",
                columns=[
                    {"name": i, "id": i, "selectable": True} for i in top_dict["data"].columns
                ],
                data=top_dict["data"].to_dict("records"),
                style_as_list_view=True,
                style_header={
                    "backgroundColor": default_color,
                    "color": "#FFFFFF",
                    "fontWeight": "bold",
                    "border": "1px solid #FFFFFF",
                },
                style_cell={
                    "textAlign": "center",
                    "color": "#888888",
                    "textOverflow": "ellipsis",
                    "maxWidth": "100px",
                    "width": "70px",
                    "border": "1px solid #F5F5F5"
                },
                style_data_conditional=[
                        {
                        # 'if': {'column_id': 'Meet Deadline', 'filter_query': '{"Meet Deadline"} = "Yes"'}, 
                        # 'color': default_color,
                        
                        'if': {"column_id": "Avg. Days before Deadline"}, "maxWidth": "50px"
                    },
                ]
            )

            return (table, round(top_dict["avg_days"], 2))

    else:
        raise PreventUpdate

