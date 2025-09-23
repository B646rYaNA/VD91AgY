# 代码生成时间: 2025-09-24 06:22:44
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import zipfile
from werkzeug.utils import secure_filename
import os

# 设置Dash应用
app = dash.Dash(__name__)

# 设置应用的布局
app.layout = html.Div([
    html.H1("文件解压工具"),
    dcc.Upload(
        id='upload-data', 
        children=html.Div(['将文件拖到这里，或者点击上传']),
        style={'lineHeight': '60px', 'borderWidth': '1px', 'borderStyle': 'dashed', 'borderRadius': '5px', 'textAlign': 'center', 'margin': '10px'},
    ),
    html.Div(id='output-data-upload'),
])

# 回调函数，处理文件上传
@app.callback(
    Output('output-data-upload', 'children'),
    [Input('upload-data', 'contents')]
)
def update_output(contents):
    if contents is not None:
        # 创建一个临时文件名
        filename = secure_filename('temp.zip')
        # 将上传的文件写入临时文件
        with open(filename, 'wb') as f:
            f.write(contents)
        try:
            # 尝试解压文件
            with zipfile.ZipFile(filename, 'r') as zip_ref:
                zip_ref.extractall('./extracted_files')
            # 返回解压成功的信息
            return '文件解压成功！'
        except zipfile.BadZipFile:
            # 处理坏的压缩文件
            return '错误：文件损坏或不是压缩文件。'
        finally:
            # 删除临时文件
            os.remove(filename)
    return '还没有上传文件。'

# 运行服务器
if __name__ == '__main__':
    app.run_server(debug=True)