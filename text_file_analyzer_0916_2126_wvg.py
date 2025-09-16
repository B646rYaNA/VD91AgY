# 代码生成时间: 2025-09-16 21:26:05
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import pandas as pd
from collections import Counter
import plotly.express as px

# Define the layout of the app
app = dash.Dash(__name__)
app.layout = html.Div(children=[
    html.H1("Text File Content Analyzer"),
    dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
        multiple=True
    ),
    html.Div(id='output-data-upload'),
    html.Div(id='file-content'),
    html.Div(id='word-count'),
    html.Div(id='word-frequency-graph')
])

# Function to extract and display file content
@app.callback(
    Output('file-content', 'children'),
    Input('upload-data', 'contents'),
    State('upload-data', 'filename')
)
def display_file_content(contents, filename):
    if contents is None:
        raise PreventUpdate
    try:
        file_content = "
".join(contents.splitlines()[:100])  # Display the first 100 lines
        return html.Pre(file_content)  # Display file content in a preformatted box
    except:
        return "Failed to display file content."

# Function to calculate and display word count
@app.callback(
    Output('word-count', 'children'),
    Input('file-content', 'children'),
    State('upload-data', 'contents')
)
def word_count(file_content):
    if file_content is None:
        raise PreventUpdate
    try:
        words = file_content.split()
        word_count_dict = Counter(words)
        return html.P(f"Total words: {len(words)}")
    except:
        return "Failed to calculate word count."

# Function to create and display word frequency graph
@app.callback(
    Output('word-frequency-graph', 'children'),
    Input('word-count', 'children'),
    State('upload-data', 'contents')
)
def word_frequency_graph(word_count, contents):
    if contents is None:
        raise PreventUpdate
    try:
        words = contents.split()
        word_count_dict = Counter(words)
        df = pd.DataFrame(list(word_count_dict.items()), columns=['Word', 'Frequency'])
        df = df.sort_values('Frequency', ascending=False)
        fig = px.bar(df, x='Frequency', y='Word', title='Word Frequency', labels={'x':'Frequency', 'y':'Word'})
        return dcc.Graph(figure=fig)
    except:
        return "Failed to create word frequency graph."

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)