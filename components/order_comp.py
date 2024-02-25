import dash
from dash import html, dcc
import dash_mantine_components as dmc
from dash_iconify import DashIconify 
from dash_mantine_components.theme import DEFAULT_COLORS

from components.utils import (
    config_plotly,
    delivery_status, 
    delivery_status_data, 
    delivery_status_info,
    default_color
)


def status_summary():

    def col_title(title: str):
        return html.P(title, className="ord-s_title")

    def over_card_info(card_id: str):
        """ 
        """
        return dmc.HoverCard(
            withArrow=True,
            shadow="md",
            children=[
                dmc.HoverCardTarget(DashIconify(icon="solar:info-square-broken", height=20)),
                dmc.HoverCardDropdown(
                    [
                        dmc.Text(delivery_status_info[str.lower(card_id)])
                    ],
                    style={"maxWidth": "200px"}
                )
            ]
        )

    def add_value(id: str):
        return html.P("0000", className="ord-s_value", id=f"{id}_status")
    
    def add_modal_link(modal_id: str):
        return html.Div(
            [
                dmc.ActionIcon(
                    DashIconify(icon="fluent-mdl2:navigate-external-inline", color=default_color, height=25),
                    size="lg",
                    variant="light",
                    id=f"{modal_id}_trigger",
                    color=DEFAULT_COLORS["teal"][0]
                ),

                dmc.Modal(
                    # title="",
                    id=f"{modal_id}_modal",
                    zIndex=10000,
                    size="lg",
                    children=[
                        html.Div(
                            [
                                html.P(str.title(modal_id), className="ord-modal_title"),
                                html.Div(
                                    [
                                        dcc.Graph(
                                            id=f"{modal_id}_month_chart", 
                                            config=config_plotly, 
                                            style={'height': "400px"}
                                        )
                                    ],
                                    className="ord-modal_figure"
                                )
                            ],
                            className="ord-modal_content_container"
                        )
                    ]
                )
            ], 
            className="ord-s_modal_trigger"
        )


    return html.Div(
        [
            dmc.Grid(
                [
                    dmc.Col(
                        [col_title("Order Status")] + [
                            html.Div(
                                [
                                    html.P(status, className=f"ord-s_name {status}"),
                                    over_card_info(status)
                                ],
                                className=f"ord-s_name_container {status}"
                            ) for status in delivery_status_data
                        ],
                        span=5,
                        className="ord-s_label_col"
                    ),
                    dmc.Col(
                        [col_title("No. Orders")] + [add_value(status) for status in delivery_status],
                        span=4,
                        className="ord-s_value_col"
                    ),
                    dmc.Col(
                        [col_title("Charts")] + [add_modal_link(status) for status in delivery_status],
                        span=3,
                        className="ord-s_modal_link_col"
                    ),
                ],
                gutter="md"
            )
        ],
        className="ord-status_container"
    )

