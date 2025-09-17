# 代码生成时间: 2025-09-18 07:58:52
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from dash.dependencies import Input, Output
import os
from glob import glob

# Constants for the app
APP_TITLE = "CSV Batch Processor"
UPLOAD_FOLDER = "uploads/"

# Initialize the Dash application
app = dash.Dash(__name__)

# App layout
app.layout = html.Div(children=[
    html.H1(APP_TITLE),
    dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
        multiple=True,
    ),
    html.Div(id='output-container'),
])

# Callback to update the output when new files are uploaded
@app.callback(Output('output-container', 'children'),
              Input('upload-data', 'contents'))
def process_files(contents):
    if contents is None:
        return "Please upload CSV files."

    # Create the uploads directory if it doesn't exist
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    # List to store processed file names
    processed_files = []
    for i, content in enumerate(contents):
        try:
            filename = content.filename
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            with open(file_path, 'wb') as file:
                file.write(content.encode())
            # Process the uploaded CSV file
            process_csv(file_path)
            processed_files.append(filename)
        except Exception as e:
            return f"An error occurred while processing the file {filename}: {str(e)}"

    # Return the list of processed files
    return "Processed files: " + ", ".join(processed_files)

# Function to process a single CSV file
def process_csv(file_path):
    # Read the CSV file into a pandas DataFrame
    try:
        df = pd.read_csv(file_path)
        # Perform any necessary processing on the DataFrame
        # For example, you could apply transformations, filters, etc.
        # This function should be expanded to include specific processing steps
        print(f"File {file_path} has been processed successfully.")
    except pd.errors.EmptyDataError:
        print(f"File {file_path} is empty.")
    except pd.errors.ParserError:
        print(f"File {file_path} could not be parsed.")
    except Exception as e:
        print(f"An error occurred while processing file {file_path}: {str(e)}")

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
