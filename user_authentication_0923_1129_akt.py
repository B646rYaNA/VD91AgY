# 代码生成时间: 2025-09-23 11:29:24
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from flask import session
from werkzeug.security import generate_password_hash, check_password_hash

# 假设用户数据存储在内存（Python字典）中，实际应用中应使用数据库
users = {
    "admin": generate_password_hash("admin123")
}

# 身份验证函数
def authenticate(username, password):
    if username in users and check_password_hash(users[username], password):
        session["username"] = username
        return True
    else:
        return False

# Dash应用程序
app = dash.Dash(__name__)

# 用户登录界面
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

# 回调函数处理用户登录
@app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')],
    [State('page-content', 'children')]
)
def display_page(pathname, page_content):
    if pathname == '/login':
        return html.Div([
            html.H3("登录"),
            html.Div([
                html.Label("用户名: "),
                dcc.Input(id='username', type='text')
            ]),
            html.Div([
                html.Label("密码: "),
                dcc.Input(id='password', type='password')
            ]),
            html.Button("登录", id='login-button', n_clicks=0),
            html.Div(id='login-response')
        ])
    elif pathname == '/dashboard':
        if 'username' in session:
            return html.Div(["欢迎回来, " + session['username'] + "!"])
        else:
            return html.Div([
                html.P("您没有权限访问这个页面。"),
                html.A("返回登录", href='/login')
            ])
    else:
        return html.Div([
            html.P("页面不存在。"),
            html.A("返回登录", href='/login')
        ])

# 登录按钮回调函数
@app.callback(
    Output('login-response', 'children'),
    [Input('login-button', 'n_clicks')],
    [State('username', 'value'), State('password', 'value')]
)
def login(n_clicks, username, password):
    if n_clicks > 0:
        if authenticate(username, password):
            return "登录成功！"
        else:
            return "无效的用户名或密码。"
    return None

# 启动服务器
if __name__ == '__main__':
    app.run_server(debug=True)