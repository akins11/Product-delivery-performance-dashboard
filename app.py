from dash import Dash, html, dcc, page_container
import dash_mantine_components as dmc
from pandas import read_csv


app = Dash(
    __name__, 
    use_pages=True,
    external_stylesheets=[
        # Google fonts
        "https://fonts.googleapis.com/css2family=Inter:wght@100;200;300;400;500;600;900&display=swap"
    ],
)
server = app.server

orders_data = read_csv("data/orders.csv")
customers_data = read_csv("data/customers.csv")
item_sellers_data = read_csv("data/item_seller.csv")


app.layout = dmc.MantineProvider(
    theme={
        "fontFamily": "'Inter', sans-serif",
        "primaryColor": "teal",
    },
    inherit=True,
    withGlobalStyles=True,
    withNormalizeCSS=True,

    children=[
        html.Div(
            [
                dcc.Store(id="store_orders_data", data=orders_data.to_dict('records')),
                dcc.Store(id="store_customer_data", data=customers_data.to_dict('records')),
                dcc.Store(id="store_seller_data", data=item_sellers_data.to_dict('records')),
                page_container
            ],
            className="dashboard-body"
        )
    ]
)

if __name__ == '__main__':
    app.run_server(debug=False)
    # app.run(debug=True)