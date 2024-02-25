import dash
from dash import html
import dash_mantine_components as dmc
from dash_iconify import DashIconify 
from dash_mantine_components.theme import DEFAULT_COLORS

from components.utils import default_color

def stats_card(stats_type: str):
    """ 
    stats_type: ["orders", "customer"]
    """

    title_str = str.title(stats_type)
    title_str = title_str if stats_type == "orders" else f"{title_str}s"
    
    return html.Div(
        [
            html.Div(
                [
                    html.P(title_str, className="ord-sc_title"),
                    html.P("0000", id=f"{stats_type}_count_value", className="ord-sc-value"),
                    html.Div(
                        [
                            html.P(
                                [ 
                                    html.Span("00", id=f"{stats_type}_percent_change", className="ord-sc-percent-text"),
                                    "%"
                                ],
                                className="ord-sc-percent"
                            ),
                            html.Div(children=[], id=f"{stats_type}_change_icon", className="ord-sc_icon")
                        ],
                        className="ord-sc_change"
                    )
                ],
                className="ord-sc_value_column"
            ),
            html.Div(
                [
                    dmc.RingProgress(
                        id=f"{stats_type}_percent_chart_value",
                        sections=[{"value": 0, "color": default_color}],
                        label=dmc.Center(dmc.Text("0%", color=default_color, id=f"{stats_type}_percent_text")),
                        size=80,
                        thickness=5
                    ),
                    html.P(f"Of total {title_str}", className="ord-sc_percent_title"),
                ],
                className="ord-sc_graph_column"
            )
        ],
        className="ord-stats_card count"
    )


def mtd_card():
    """ 
    """

    return html.Div(
        [
            html.Div(
                [
                    dmc.Tooltip(
                        label="Month to Date (Number of Orders)",
                        position="left",
                        withArrow=True,
                        children=[
                            DashIconify(icon="solar:info-square-linear", color=default_color, height=20)
                        ]
                    )
                ],
                className="ord-mt_tooltip_container"
            ),

            html.Div(
                [
                    html.P("MTD", className="ord-mtd_title"),
                    html.P("00000", id="order_mtd", className="ord-mtd_value")
                ],
                className="ord-mtd_content"
            ),
            html.P("Jan - Aug", id="order_mtd_month_abbr_name_range", className="ord-m_bottom_text")
        ],
        className="ord-stats_card mtd"
    )


def mom_card():
    """ 
    """

    return html.Div(
        [
            html.Div(
                [
                    dmc.Tooltip(
                        label="Month over Month",
                        position="left",
                        withArrow=True,
                        children=[
                            DashIconify(icon="solar:info-square-linear", color=default_color, height=20)
                        ]
                    )
                ],
                className="ord-mt_tooltip_container"
            ),
            html.Div(
                [
                    html.P("MoM", className="ord-mtd_title"),
                    html.Div(
                        [
                            html.Div(
                                DashIconify(icon="bi:dash-circle", color=default_color, height=20),
                                id="mom_icon_type",
                                className="ord-mom_icon_container"
                            ),
                            html.P(
                                [html.Span("00", id="order_mom", className="ord-mom_value_text"), "%"],
                                className="ord-mom_value"
                            )
                        ],
                        className="ord-mom_value_container"
                    )
                ],
                className="ord-mtd_content"
            ),
            html.P(
                [
                    html.Span("00", id="order_mom_growth_rate", className="ord-mom_gr_value"),
                    html.Span("%", className="ord-mom_gr_percent"),
                    " Growth rate"
                ],
                className="ord-m_bottom_text"
            )
        ],
        className="ord-stats_card mtd"
    )


def seller_stats_card():
    return html.Div(
        [
            html.Div(
                [
                    html.P("No. Sellers:", className="sp-s_title"),
                    html.P("0000", id="seller_count", className="sp-s_value")
                ],
                className="sp-s_counts"
            ),
            html.Div(
                [
                    html.P("Total Sellers:", className="sp-s_title total"),
                    html.P("0000", id="total_seller_count", className="sp-s_value total")
                ],
                className="sp-s_counts"
            ),
            dmc.RingProgress(
                id="seller_percentage_chart",
                sections=[{"value": 0, "color": default_color}],
                label=dmc.Center(dmc.Text("0%", id="seller_percent_text_value", color=default_color, size=50)),
                size=300,
                thickness=20,
                roundCaps=True,
                className="sp-s_progressbar"
            ),
            dmc.Text("Of Total Sellers", className="sp-s_pb_text")
        ],
        className="sp-stats_container"
    )