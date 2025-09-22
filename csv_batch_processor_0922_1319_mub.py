# 代码生成时间: 2025-09-22 13:19:34
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
import os

# 定义CSV文件批量处理器类
class CSVBatchProcessor:
    def __init__(self, app, upload_folder):
        # 初始化Dash应用和上传文件夹
        self.app = app
        self.upload_folder = upload_folder
        
        # 定义布局
        self.layout()
        
    def layout(self):
        # 定义Dash应用布局
        self.app.layout = html.Div([
            html.H1('CSV文件批量处理器'),
            dcc.Upload(
                id='upload-data',
                children=html.Button('上传CSV文件'),
                multiple=True,
                accept='.csv'
            ),
            html.Div(id='output')
        ])
        
    # 定义回调函数处理上传的CSV文件
    @staticmethod
    def process_uploaded_file(uploaded_file):
        # 读取上传的CSV文件
        if uploaded_file.filename:
            try:
                return pd.read_csv(uploaded_file)
            except Exception as e:
                raise PreventUpdate(f"Error processing file {uploaded_file.filename}: {str(e)}")
        raise PreventUpdate("No file selected")
    
    # 定义回调函数显示上传文件的内容
    @staticmethod
    def update_output(uploaded_file):
        # 处理上传的文件并显示内容
        dataframe = CSVBatchProcessor.process_uploaded_file(uploaded_file)
        if dataframe is not None:
            return px.display(dataframe)
        raise PreventUpdate()
        
# 初始化Dash应用
app = dash.Dash(__name__)
app.config.suppress_callback_exceptions = True
app.config.static_folder = 'static'

# 设置上传文件夹
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.mkdir(UPLOAD_FOLDER)

# 创建CSV文件批量处理器实例
processor = CSVBatchProcessor(app, UPLOAD_FOLDER)

# 定义回调函数
@app.callback(
    Output('output', 'children'),
    [Input('upload-data', 'contents')],
    [State('upload-data', 'filename')]
)
def update_output(contents, filename):
    return CSVBatchProcessor.update_output(contents)

# 运行Dash应用
if __name__ == '__main__':
    app.run_server(debug=True)