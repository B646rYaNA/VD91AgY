# 代码生成时间: 2025-10-13 23:08:57
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

# 定义一个函数来加载数据
def load_data():
    # 假设数据存储在CSV文件中
    data = pd.read_csv('teaching_quality_data.csv')
    return data

# 创建Dash应用
app = dash.Dash(__name__)

# 定义应用的布局
app.layout = html.Div([
    html.H1("教学质量分析"),
    dcc.Dropdown(
        id='subject-dropdown',
        options=[{"label": subject, "value": subject} for subject in load_data().columns],
        value=load_data().columns[0],
        clearable=False
    ),
    dcc.Graph(id='quality-graph')
])

# 定义回调函数来更新图表
@app.callback(
    Output('quality-graph', 'figure'),
    [Input('subject-dropdown', 'value')]
)
def update_graph(selected_subject):
    # 加载数据
    data = load_data()
    
    # 检查选择的主题是否存在
    if selected_subject not in data.columns:
        raise ValueError("Selected subject does not exist in data")
    
    # 创建图表
    fig = px.line(data, x='date', y=selected_subject, title=f'{selected_subject} Quality Over Time')
    return fig

# 运行应用
if __name__ == '__main__':
    app.run_server(debug=True)