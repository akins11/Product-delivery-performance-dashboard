from dash import html, dcc
from dash_iconify import DashIconify 
import dash_mantine_components as dmc
from dash_mantine_components.theme import DEFAULT_COLORS

from components.utils import delivery_phase_data, config_plotly, period_data, default_color

def breadcrumb():
    """ 
    """

    def bc_item(item_customer: bool, title: str, id: str):
        if item_customer:
            bc_icon = DashIconify(icon="fluent:person-12-filled", color=default_color, height=20)
        else:
            bc_icon = DashIconify(
                icon="solar:double-alt-arrow-right-outline", color=DEFAULT_COLORS["gray"][6], height=20
            )

        return html.Div(
            [
                html.P(title, className="dp-bc_item-title"), 
                bc_icon
            ], 
            className="dp-bc_item",
            id=id
        )

    return html.Div(
        [
            bc_item(False, "Order Placement", "placement"),
            bc_item(False, "Approval", "approval"),
            bc_item(False, "Carrier", "carrier"),
            bc_item(True, "Customer", "customer")
        ],
        className="dp-breadcrumb"
    )


def phase_selection():

    def add_item(name: str):
        return html.Div(
            [
                html.P(name, className="dp-ps_title"),
                DashIconify(icon="ep:arrow-down-bold", color=default_color, height=15)
            ],
            className="dp-ps_item"
        )
    
    def hover_item(target, id: str, label: str, value):
        return dmc.HoverCard(
            shadow="md",
            withArrow=True,
            children=[
                dmc.HoverCardTarget(target),
                dmc.HoverCardDropdown(
                    dmc.Select(
                        label=label,
                        placeholder=f"Select ....",
                        id=f"{id}_phase",
                        searchable=True,
                        clearable=False,
                        value=value,
                        data=delivery_phase_data,
                        style={"width": 200},
                        icon=DashIconify(icon="radix-icons:magnifying-glass")
                    )
                )
            ]
        )
    

    return html.Div(
        [
            html.P("Delivery phase:", className="dp-ps_phase_title"),
            hover_item(
                add_item("From"),
                id="from",
                label="Begin delivery phase @",
                value="placement"
            ),
            hover_item(
                add_item("To"),
                id="to",
                label="End delivery phase @",
                value="customer"
            )
        ],
        className="dp-ps_container"
    )


def unit_of_time_table():

    def add_label(label: str):
        lc_label = str.lower(label)

        return html.Div(
            [html.P(label, className=f"dp-ut_label {lc_label}")],
            className=f"dp-ut_label_container {lc_label}"
        )

    def add_count(value: str, id: str):
        return html.P(value, className="dp-ut_count", id=f"{id}_count")
    
    def add_percentage(value: float, id: str):
        return html.P(
            [
                html.Span(value, className="dp-ut_percent_value", id=f"{id}_percent"),
                "%"
            ],
            className="dp-ut_percent"
        )
    
    return html.Div(
        [
            dmc.Grid(
                [
                    dmc.Col(
                        [
                            html.P("Unit of Time", className="dp-ut_title"),
                            add_label("Seconds"),
                            add_label("Minutes"),
                            add_label("Hours"),
                            add_label("Days"),
                        ],
                        span=4,
                    ),

                    dmc.Col(
                        [
                            html.P("No. Transactions", className="dp-ut_title"),
                            add_count("0000", "second"),
                            add_count("0000", "minute"),
                            add_count("00", "hour"),
                            add_count("00", "day"),
                        ],
                        span=5,
                    ),

                    dmc.Col(
                        [
                            html.P(
                                ["Proportion", html.Span(" (%)", className="dp_ut_title_s")], 
                                className="dp-ut_title"
                            ),
                            add_percentage("00", "second"),
                            add_percentage("00", "minute"),
                            add_percentage("00", "hour"),
                            add_percentage("00", "day"),
                        ],
                        span=3,
                    )
                ]
            )
        ],
        className="dp-unit_time"
    )



def figure_output_ui(chart_id: str, period_value: str="hour"):
    """ 
    """

    return html.Div(
        [
            html.Div(
                [
                    dmc.HoverCard(
                        withArrow=True,
                        shadow="md",
                        children=[
                            dmc.HoverCardTarget(
                                dmc.Avatar(DashIconify(icon="gala:settings", height=20), radius="md"), #color="blue",
                            ),
                            dmc.HoverCardDropdown(
                                [
                                    dmc.SegmentedControl(
                                        orientation="vertical",
                                        id=f"{chart_id}_period",
                                        value=period_value,
                                        data=[{"value": v, "label": str.title(v)} for v in period_data],
                                        color=DEFAULT_COLORS["teal"]
                                    )
                                ]
                            )
                        ]
                    )
                ],
                className="dp-chart-settings_container"
            ),

            dcc.Graph(id=chart_id, config=config_plotly, style={'height': "350px"}),
        ],
        className="dp-chart"
    )










