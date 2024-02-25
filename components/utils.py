import calendar
from dash_mantine_components.theme import DEFAULT_COLORS

default_color = DEFAULT_COLORS["teal"][4]

month_names = list(calendar.month_name[1:9])
month_name_data = [{"value": name, "label": name} for name in month_names]

delivery_phase = ["placement", "approval", "carrier", "customer"]
delivery_phase_data = [{"value": i, "label": str.capitalize(i)} for i in delivery_phase]

delivery_status = ["delivered", "shipped", "canceled", "unavailable", "invoiced"]
delivery_status_data = [str.capitalize(status) for status in delivery_status]

delivery_status_info = {
    "delivered": "The product has been physically delivered to the customer.",
    "shipped": "The product has left the origin location and is in transit to the customer.",
    "canceled": "The order has been terminated and will not be delivered.",
    "unavailable": "The ordered item is unavailable to fulfill the order.",
    "invoiced": "A bill has been issued for the order",
}

# A dictionary of full month name as the key and their respective abbrivations as value.
month_abbrev = {calendar.month_name[i]: abbrev for i, abbrev in enumerate(calendar.month_abbr[1:], start=1)}

# Default data filter variable
default_date_variable = "order_purchase_timestamp"

# period
period_data = ["second", "minute", "hour", "day", "week"]

config_plotly = {
    "displaylogo": False,
    "modeBarButtonsToRemove": ['pan2d', 'lasso2d', 'zoom2d', 'zoomIn2d', 'zoomOut2d', 'select2d', 'autoScale2d']
}
