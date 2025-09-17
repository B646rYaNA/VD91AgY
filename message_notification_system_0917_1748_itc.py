# 代码生成时间: 2025-09-17 17:48:06
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from flask import Flask
import threading
import time
import random
import logging

# 设置日志配置
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 初始化Dash应用
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server
app.config.suppress_callback_exceptions = True

# 定义全局变量
MESSAGE_QUEUE = []
LOCK = threading.Lock()

# 定义回调函数来更新消息队列
@app.callback(
    Output('message-container', 'children'),
    [Input('submit-button', 'n_clicks')],
    [State('message-input', 'value')]
)
def update_message_queue(n_clicks, message):
    if n_clicks is None:
        return []
    with LOCK:
        MESSAGE_QUEUE.append(message)
    return []

# 定义回调函数来显示消息队列中的消息
@app.callback(
    Output('display-messages', 'children'),
    [Input('interval-component', 'n_intervals')],
    [State('message-container', 'children')]
)
def display_messages(n_intervals, children):
    with LOCK:
        messages = MESSAGE_QUEUE.copy()
        MESSAGE_QUEUE.clear()
    return [html.Div([html.P(f'Message: {msg}'), html.Br()], style={'whiteSpace': 'pre-line'}) for msg in messages]

# 定义布局
app.layout = html.Div([
    dbc.Container([
        dbc.Row([
            dbc.Col([dbc.Input(type='text', id='message-input', placeholder='Enter a message')], width=6),
            dbc.Col([dbc.Button('Submit', id='submit-button', color='primary')], width=2)
        ], align='center'),
        dbc.Row([
            dbc.Col([dcc.Interval(id='interval-component', interval=1*1000)], width=12)
        ], align='center'),
        dbc.Row([
            dbc.Col([html.Div(id='display-messages')], width=12)
        ], align='center'),
        dbc.Row([
            dbc.Col([html.Div(id='message-container')], width=12)
        ], align='center')
    ], fluid=True)
])

# 定义后台线程来模拟消息生成
def background_thread():
    while True:
        time.sleep(5)  # 每5秒生成一条消息
        message = f'Random message {random.randint(1, 100)}'
        with LOCK:
            MESSAGE_QUEUE.append(message)
        logger.info(f'Generated message: {message}')

# 启动后台线程
thread = threading.Thread(target=background_thread)
thread.start()

# 定义错误处理
@app.server.errorhandler(Exception)
def handle_exception(e):
    return str(e), 500

# 启动Dash应用
if __name__ == '__main__':
    app.run_server(debug=True)
