# 代码生成时间: 2025-09-21 04:12:29
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import zipfile
import os
import io
from werkzeug.utils import secure_filename
from flask import send_from_directory

# 压缩文件解压工具的Dash应用
class DecompressionApp:
    def __init__(self):
        self.app = dash.Dash(__name__)
        self.layout()
        self.callbacks()

    def layout(self):
        # 应用的布局
        self.app.layout = html.Div(children=[
            html.H1(children='压缩文件解压工具'),
            html.Div(children=[
                dcc.Upload(
                    id='upload-data',
                    children=html.Button('选择文件'),
                    multiple=True,
                    max_size=2000*1024*1024  # 最大文件大小设置为2MB
                ),
            ]),
            html.Div(id='output-data-upload'),
            html.Button('解压文件', id='decompress-button', n_clicks=0),
            html.Div(id='output-decompress'),
        ])

    def callbacks(self):
        # 回调函数
        @self.app.callback(
            Output('output-data-upload', 'children'),
            [Input('upload-data', 'contents')],
        )
        def update_output(listed filenames):
            if listed is not None:
                return [
                    html.H5(filename),
                    html.P(f'文件大小: {len(filenames)} bytes')]
            return []

        @self.app.callback(
            Output('output-decompress', 'children'),
            [Input('decompress-button', 'n_clicks')],
            [State('upload-data', 'contents'),
             State('upload-data', 'filename')
            ],
        )
        def decompress_files(n_clicks, contents, filenames):
            if contents is not None and n_clicks > 0:
                try:
                    # 创建一个临时目录来解压文件
                    temp_folder = 'temp_folder'
                    os.makedirs(temp_folder, exist_ok=True)

                    # 解压文件
                    for filename, file_content in zip(filenames, contents):
                        file_path = os.path.join(temp_folder, secure_filename(filename))
                        with open(file_path, 'wb') as f:
                            f.write(file_content)
                        self._decompress(file_path, temp_folder)

                    # 删除临时文件
                    for file in os.listdir(temp_folder):
                        os.remove(os.path.join(temp_folder, file))
                    os.rmdir(temp_folder)

                    return [
                        html.H5('解压成功'),
                        html.Button(
                            '下载解压后的文件',
                            id='download-button',
                            n_clicks=0
                        ),
                        dcc.Download(id='download-button-content')
                    ]
                except Exception as e:
                    return [html.H5(f'解压失败: {str(e)}')]
            return []

        @self.app.callback(
            Output('download-button-content', 'data'),
            [Input('download-button', 'n_clicks')],
            [State('upload-data', 'filename')]
        )
        def download解压文件(n_clicks, filenames):
            if n_clicks > 0:
                # 创建临时压缩文件
                temp_folder = 'temp_folder'
                zip_filename = 'extracted_files.zip'
                zip_path = os.path.join(temp_folder, zip_filename)
                with zipfile.ZipFile(zip_path, 'w') as zipf:
                    for file in filenames:
                        file_path = os.path.join(temp_folder, secure_filename(file))
                        zipf.write(file_path, arcname=file)

                # 删除临时文件
                for file in os.listdir(temp_folder):
                    os.remove(os.path.join(temp_folder, file))
                os.rmdir(temp_folder)

                return send_from_directory(directory=temp_folder, filename=zip_filename, as_attachment=True)

    def _decompress(self, file_path, target_folder):
        # 解压文件的辅助函数
        try:
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                zip_ref.extractall(target_folder)
        except zipfile.BadZipFile as e:
            print(f'BadZipFile: {e}')
        except Exception as e:
            print(f'Error: {e}')

    def run(self):
        self.app.run_server(debug=True)

if __name__ == '__main__':
    app = DecompressionApp()
    app.run()