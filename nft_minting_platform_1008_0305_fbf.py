# 代码生成时间: 2025-10-08 03:05:24
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
from dash.exceptions import PreventUpdate
import requests
import json
from smart_contract import NFTContract  # 假设有一个智能合约模块

# 应用布局
app = dash.Dash(__name__)
app.layout = html.Div([
    html.H1("NFT Minting Platform"),
    html.Div(id='input-group', children=[
        dcc.Input(id='nft-name', type='text', placeholder='Enter NFT name'),
        dcc.Upload(
            id='nft-upload',
            children=html.Button('Upload NFT'),
            multiple=False
        ),
        html.Button('Mint NFT', id='mint-button', n_clicks=0)
    ]),
    html.Div(id='output-container')
])

# 回调函数 - 上传文件
@app.callback(
    Output('nft-upload', 'contents'),
    [Input('nft-upload', 'contents')],
    [State('nft-upload', 'filename')]
)
def update_output(list_of_contents, list_of_names):  # 用于更新上传文件的内容
    if list_of_contents is not None:  # 检查是否有文件上传
        return list_of_contents
    raise PreventUpdate

# 回调函数 - 铸造NFT
@app.callback(
    Output('output-container', 'children'),
    [Input('mint-button', 'n_clicks')],
    [State('nft-name', 'value'), State('nft-upload', 'contents')],
)
def mint_nft(n_clicks, nft_name, file_content):  # 铸造NFT的回调函数
    if n_clicks == 0 or nft_name is None or file_content is None:  # 检查是否满足铸造条件
        raise PreventUpdate
    try:  # 尝试铸造NFT
        # 假设有一个NFTContract智能合约类，用于与区块链交互
        contract = NFTContract()
        response = contract.mint_nft(nft_name, file_content)
        if response['status']:  # 检查铸造是否成功
            return html.Div([html.P(f'NFT {nft_name} minted successfully!'), html.A('View NFT', href=response['url'])])
        else:  # 铸造失败
            return html.Div([html.P(f'Failed to mint NFT {nft_name}'), html.P(response['message'])])
    except Exception as e:  # 错误处理
        return html.Div([html.P(f'An error occurred: {str(e)}')])

if __name__ == '__main__':
    app.run_server(debug=True)