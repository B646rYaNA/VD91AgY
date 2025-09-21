# 代码生成时间: 2025-09-21 13:33:10
# inventory_management.py

# Import necessary libraries
import dash
from dash import html, dcc
from dash.dependencies import Input, Output, State
import plotly.express as px
import pandas as pd

# Initialize Dash application
app = dash.Dash(__name__)

# Define layout of the dashboard
app.layout = html.Div(children=[
    html.H1('Inventory Management System'),
    html.Div(id='inventory-container'),
    dcc.Dropdown(
        id='product-dropdown',
        options=[{'label': product, 'value': product} for product in ['Product A', 'Product B', 'Product C']],
        placeholder='Select a Product'
    ),
    dcc.Graph(id='inventory-graph'),
    html.Button('Update Inventory', id='update-button', n_clicks=0),
    dcc.Textarea(
        id='update-textarea',
        placeholder='Enter update details (e.g., +10 for increase, -5 for decrease)',
        style={'width': '100%', 'height': '100px'}
    )
])

# Initialize sample inventory data
inventory_data = pd.DataFrame(
    {
        'Product': ['Product A', 'Product B', 'Product C'],
        'Quantity': [100, 150, 200]
    }
)

# Define callback to update inventory graph
@app.callback(
    [Output('inventory-graph', 'figure'), Output('inventory-container', 'children')],
    [Input('product-dropdown', 'value')],
    [State('inventory-data', 'children')]
)
def update_inventory_graph(selected_product, inventory_data_json):
    # Parse inventory data from JSON
    inventory_data = pd.read_json(inventory_data_json)

    # Filter data for the selected product
    filtered_data = inventory_data[inventory_data['Product'] == selected_product]

    # Create a bar chart for the selected product
    fig = px.bar(filtered_data, x='Product', y='Quantity', title=f'Inventory for {selected_product}')
    fig.update_layout(margin={'l': 20, 'r': 20, 't': 30, 'b': 20})

    # Return updated graph and container children
    return fig, f'Inventory for {selected_product}: {filtered_data["Quantity"].values[0]}'

# Define callback to handle update button click
@app.callback(
    Output('inventory-data', 'children'),
    [Input('update-button', 'n_clicks')],
    [State('inventory-data', 'children'), State('update-textarea', 'value')]
)
def update_inventory(n_clicks, inventory_data_json, update_details):
    # Check if the update button was clicked
    if n_clicks > 0:
        # Parse inventory data from JSON
        inventory_data = pd.read_json(inventory_data_json)

        # Split update details into parts
        product, change = update_details.split(' ')
        change = int(change)

        # Update inventory quantity
        inventory_data.loc[inventory_data['Product'] == product, 'Quantity'] += change

        # Return updated inventory data as JSON
        return inventory_data.to_json()
    return inventory_data_json

# Define callback to update inventory graph after update
@app.callback(
    Output('inventory-graph', 'figure'),
    [Input('inventory-data', 'children')],
    [State('product-dropdown', 'value')]
)
def update_graph(inventory_data_json, selected_product):
    # Parse inventory data from JSON
    inventory_data = pd.read_json(inventory_data_json)

    # Filter data for the selected product
    filtered_data = inventory_data[inventory_data['Product'] == selected_product]

    # Create a bar chart for the selected product
    fig = px.bar(filtered_data, x='Product', y='Quantity', title=f'Inventory for {selected_product}')
    fig.update_layout(margin={'l': 20, 'r': 20, 't': 30, 'b': 20})

    # Return updated graph
    return fig

# Run the Dash application
if __name__ == '__main__':
    app.run_server(debug=True)