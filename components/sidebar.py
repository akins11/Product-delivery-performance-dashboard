from dash import html, dcc
from dash_iconify import DashIconify 
import dash_mantine_components as dmc
from dash_mantine_components.theme import DEFAULT_COLORS

def sidebar(page_id: str):

    def page_nav_links(icon_name: str, link_title: str, path: str):
        """ 
        """
        return html.Li(
            [
                html.A(
                    [
                        DashIconify(icon=icon_name, height=25),
                        link_title
                    ],
                    href=path, 
                    className="ps-a"
                )
            ],
            className="ps-link"
        )

    return html.Nav(
        [
            html.Div(
                [
                    html.H2("Delivery Insight", className="ps-title"),
                    DashIconify(icon="carbon:delivery-parcel", color=DEFAULT_COLORS["teal"][5], height=40),
                ],
                className="ps-title_icon"
            ),
            html.Ul(
                [
                    page_nav_links("lucide:shopping-bag", "Order", "/"),
                    page_nav_links("iconamoon:delivery-fill", "Duration", "/durations"),
                    page_nav_links("mdi:users-group", "Sellers", "/seller"),
                    dmc.Tooltip(
                        withArrow=True,
                        label = "Log-Out",
                        position="right",
                        children=[
                            html.Div(
                                DashIconify(icon="carbon:logout", color=DEFAULT_COLORS["dark"][9], height=30),
                                className="ps-log_out_container"
                            ),
                        ]
                    ),
                ],
                className="ps-link_list"
            )
        ],
        className="page-sidebar close",
        id=f"{page_id}_sidebar"
    )

