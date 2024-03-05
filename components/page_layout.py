from dash import html, dcc
import dash_mantine_components as dmc
from dash_iconify import DashIconify 
from dash_mantine_components.theme import DEFAULT_COLORS

from components.sidebar import sidebar
from components.utils import month_name_data, config_plotly


def dashboard_page_layout(
        page_name_id: str,
        page_title: str,
        page_content: html.Div
):
    """ 
    """

    return html.Div(
        [
            sidebar(page_name_id),

            html.Main(
                [
                    # Toggle btn
                    dmc.Burger(
                        id=f"{page_name_id}_open_burger", 
                        opened=False, 
                        size="sm",
                        color="gray",
                        className="sidebar_toggle_button"
                    ),
                    
                    html.Div(
                        [
                            html.H2(page_title, className="pmc-title"),
                            html.Div(
                                [
                                    html.P("Month:", className="pmc-select-title"),
                                    dmc.Select(
                                        label="",
                                        placeholder="Select Month",
                                        id=f"{page_name_id}_selected_month",
                                        searchable=True,
                                        clearable=False,
                                        value="August",
                                        data=month_name_data,
                                        style={"width": 200},
                                        icon=DashIconify(icon="radix-icons:magnifying-glass")
                                    ),
                                ],
                                className="pmc-info"
                            )
                        ],
                        className="pmc-header"
                    ),

                    page_content
                ],
                className="page-main-content"
            )
        ],
        className="page-container",
        id=page_name_id
    )




def graph_container(id: str, graph_height: str="370px"):
    """ 
    """
    return html.Div(
        dcc.Graph(id=id, config=config_plotly, style={'height': graph_height}),
        className="graph-container"
    )



def grid_container(children: list=None, id: str=""):
    """ 
    """
    return html.Div(children=children, id=id, className="c-grid")


def grid_col(children: list=None, id: str="", span: int=6) -> list:
    """ 
    """
    return html.Div(children=children, id=id, className=f"span-{span}")