# 代码生成时间: 2025-10-01 03:24:30
import dash
# NOTE: 重要实现细节
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
from dash.dependencies import Input, Output, State
import numpy as np
import pandas as pd
from scipy.stats import norm, uniform, expon

# Probability Distribution Calculator App
class ProbabilityDistributionCalculator:
    def __init__(self, name, server):
        # Initialize the Dash application
        self.app = dash.Dash(name=name, server=server)
        self.app.layout = html.Div([
            html.H1("Probability Distribution Calculator"),
            html.Div([
                dcc.Dropdown(
                    id="distribution-type",
                    options=[
                        {'label': 'Normal', 'value': 'normal'},
                        {'label': 'Uniform', 'value': 'uniform'},
                        {'label': 'Exponential', 'value': 'exponential'}
                    ],
                    value='normal'  # Default value
                ),
# TODO: 优化性能
                dcc.Input(id="mean", type="number", placeholder="Mean"),
                dcc.Input(id="std-dev", type="number", placeholder="Standard Deviation"),
                dcc.Input(id="min-value", type="number", placeholder="Minimum Value"),
# 优化算法效率
                dcc.Input(id="max-value", type="number", placeholder="Maximum Value"),
# 添加错误处理
                dcc.Input(id="rate", type="number", placeholder="Rate")
            ], style={'width': '48%', 'display': 'inline-block'}),
            dcc.Graph(id="distribution-graph")
        ])

        # Define callback for updating the graph
# 改进用户体验
        @self.app.callback(
            Output("distribution-graph", "figure"),
            [Input("distribution-type", "value"),
             Input("mean", "value"),
             Input("std-dev", "value"),
             Input("min-value", "value"),
             Input("max-value", "value"),
             Input("rate", "value")
            ],
            prevent_initial_call=True
        )
        def update_graph(distribution_type, mean, std_dev, min_value, max_value, rate):
            # Check for valid input and handle errors
            if distribution_type == 'normal':
                if mean is None or std_dev is None:
                    return px.line().update_layout(title="Please provide mean and standard deviation.")
# 优化算法效率
                data = np.linspace(mean - 3 * std_dev, mean + 3 * std_dev, 1000)
                y = norm.pdf(data, mean, std_dev)
# 改进用户体验
            elif distribution_type == 'uniform':
                if min_value is None or max_value is None:
                    return px.line().update_layout(title="Please provide minimum and maximum values.")
                data = np.linspace(min_value, max_value, 1000)
                y = uniform.pdf(data, min_value, max_value - min_value)
            elif distribution_type == 'exponential':
                if rate is None:
                    return px.line().update_layout(title="Please provide rate.")
                data = np.linspace(0, 10, 1000)
# NOTE: 重要实现细节
                y = expon.pdf(data, scale=1/rate)
            else:
                return px.line().update_layout(title="Invalid distribution type.")

            # Create a line plot
            fig = px.line(x=data, y=y, title=f"{distribution_type.capitalize()} Distribution")
            return fig

# Run the app if this script is executed directly
if __name__ == '__main__':
    app = ProbabilityDistributionCalculator(__name__, server=None)
    app.app.run_server(debug=True)