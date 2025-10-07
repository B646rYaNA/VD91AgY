# 代码生成时间: 2025-10-07 18:01:49
import dash
import dash_core_components as dcc
import dash_html_components as html
import requests
from dash.dependencies import Input, Output, State

# API测试工具的Dash应用
class APITestTool:
    def __init__(self, app):
        self.app = app
        self.layout()
        self.callback()

    def layout(self):
        """定义Dash应用的布局"""
        self.app.layout = html.Div(children=[
            html.H1(children='API测试工具'),
            html.Div(children=[
                dcc.Input(id='api-url', type='text', placeholder='请输入API地址'),
                dcc.Select(id='method', options=[{'label': i, 'value': i} for i in ['GET', 'POST', 'PUT', 'DELETE']], value='GET'),
                html.Button('发送请求', id='send-button', n_clicks=0),
                dcc.Textarea(id='response', placeholder='响应内容会显示在这里')
            ]),
        ])

    def callback(self):
        """注册回调函数"""
        @self.app.callback(
            Output('response', 'value'),
            [Input('send-button', 'n_clicks')],
            prevent_initial_call=True,
            [State('api-url', 'value'), State('method', 'value')]
        )
        def send_request(n_clicks, api_url, method):
            """发送API请求并返回响应内容"""
            if n_clicks == 0:
                return ''
            try:
                if method == 'GET':
                    response = requests.get(api_url)
                elif method == 'POST':
                    response = requests.post(api_url)
                elif method == 'PUT':
                    response = requests.put(api_url)
                elif method == 'DELETE':
                    response = requests.delete(api_url)
                else:
                    raise ValueError('不支持的HTTP方法')
                return response.text
            except requests.RequestException as e:
                return f'请求失败：{e}'
            except Exception as e:
                return f'发生错误：{e}'

# 创建Dash应用
app = dash.Dash(__name__)
api_test_tool = APITestTool(app)

if __name__ == '__main__':
    app.run_server(debug=True)