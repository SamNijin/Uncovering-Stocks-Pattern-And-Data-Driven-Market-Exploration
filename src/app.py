import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output
from dash.dependencies import Input, Output
from plotly.subplots import make_subplots
import plotly.graph_objects as go

# Sample stock and revenue data (replace with your actual data)
stock_data_df = pd.read_csv('extracted-datasets/tesla-stocks.csv')  # Replace with your data
tesla_revenue = pd.read_csv('extracted-datasets/tesla-revenue.csv')  # Replace with your data
gme_df = pd.read_csv('extracted-datasets/game-stop-stocks.csv')  # Replace with your data
gme_revenue = pd.read_csv('extracted-datasets/game-stop-revenue.csv')  # Replace with your data

def make_graph(stock_data, revenue_data, stock):
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, subplot_titles=("Historical Share Price", "Historical Revenue"), vertical_spacing=.3)
    stock_data_specific = stock_data[stock_data.Date <= '2021-06-14']
    revenue_data_specific = revenue_data[revenue_data.Date <= '2021-04-30']
    fig.add_trace(go.Scatter(x=pd.to_datetime(stock_data_specific.Date), y=stock_data_specific.Close.astype("float"), name="Share Price"), row=1, col=1)
    fig.add_trace(go.Scatter(x=pd.to_datetime(revenue_data_specific.Date), y=revenue_data_specific.Revenue.astype("float"), name="Revenue"), row=2, col=1)
    fig.update_xaxes(title_text="Date", row=1, col=1)
    fig.update_xaxes(title_text="Date", row=2, col=1)
    fig.update_yaxes(title_text="Price ($US)", row=1, col=1)
    fig.update_yaxes(title_text="Revenue ($US Millions)", row=2, col=1)
    fig.update_layout(showlegend=False, height=900, title=stock, xaxis_rangeslider_visible=True)
    return fig

# Create a Dash app
app = Dash(__name__)
server=app.server
app.layout = html.Div([
    html.H1("Stock Visualization Dashboard", style={'text-align':'center'}),
    dcc.Dropdown(
        id='stock-dropdown',
        options=[
            {'label': 'Tesla', 'value': 'Tesla'},
            {'label': 'Game Stocks', 'value': 'Game Stocks'}
        ],
        value='Tesla'
    ),
    dcc.Graph(id='stock-graph'),

html.Div([
        html.Hr(),  # Horizontal line
        html.P("© 2023 Sam Nijin", style={'text-align': 'center', 'padding-top':'25px'}),
        # html.P("Sam Nijin", style={'text-align': 'center'}),
    ], style={'margin-top': '20px', 'padding': '10px'}),
])


@app.callback(Output('stock-graph', 'figure'), [Input('stock-dropdown', 'value')])
def update_graph(selected_stock):
    if selected_stock == 'Tesla':
        return make_graph(stock_data_df, tesla_revenue, selected_stock)
    elif selected_stock == 'Game Stocks':
        return make_graph(gme_df, gme_revenue, selected_stock)

if __name__ == '__main__':
    app.run_server(debug=False)
