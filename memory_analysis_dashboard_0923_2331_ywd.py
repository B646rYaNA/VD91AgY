# 代码生成时间: 2025-09-23 23:31:40
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import psutil
import plotly.express as px
import pandas as pd

# 定义内存分析类
class MemoryAnalysisDashboard:
    def __init__(self):
        # 初始化Dash应用
        self.app = dash.Dash(__name__)

        # 设置Dash应用布局
        self.app.layout = html.Div(
            children=[
                html.H1(children='Memory Usage Analysis Dashboard'),
                dcc.Dropdown(
                    id='interval-dropdown',
                    options=[
                        {'label': '1s', 'value': '1s'},
                        {'label': '5s', 'value': '5s'},
                        {'label': '10s', 'value': '10s'}
                    ],
                    value='1s'
                ),
                dcc.Graph(id='memory-usage-graph')
            ]
        )

        # 定义回调函数
        @self.app.callback(
            Output('memory-usage-graph', 'figure'),
            [Input('interval-dropdown', 'value')]
        )
        def update_memory_usage_graph(selected_interval):
            # 收集内存使用情况数据
            memory_data = self.collect_memory_data(selected_interval)
            # 创建图表
            figure = px.line(memory_data, x='timestamp', y='memory_usage', title='Memory Usage Over Time')
            return figure

        # 设置回调函数的定时器
        self.app.callback_manager.timers.append(
            timer=
            {
                'interval': 1 * 1000,  # 每1秒执行一次
                'immediate': True,
                'callback': update_memory_usage_graph,
                'args': ['1s']  # 默认参数
            }
        )

    def collect_memory_data(self, interval):
        """
        收集内存使用情况数据
        :param interval: 收集间隔（秒）
        :return: 内存使用情况数据（Pandas DataFrame）
        """
        try:
            # 初始化数据列表
            data = []
            # 收集数据
            for _ in range(10):  # 收集10个数据点
                current_timestamp = pd.to_datetime('now')
                memory_usage = psutil.virtual_memory().percent
                data.append({'timestamp': current_timestamp, 'memory_usage': memory_usage})
                time.sleep(int(interval))  # 等待指定的间隔时间
            # 将数据转换为Pandas DataFrame
            memory_data = pd.DataFrame(data)
            return memory_data
        except Exception as e:
            # 错误处理
            print(f'Error collecting memory data: {e}')
            return pd.DataFrame()

    def run(self, host='0.0.0.0', port=8050):
        # 运行Dash应用
        self.app.run_server(host=host, port=port)

# 实例化并运行内存分析仪表板
if __name__ == '__main__':
    memory_dashboard = MemoryAnalysisDashboard()
    memory_dashboard.run()