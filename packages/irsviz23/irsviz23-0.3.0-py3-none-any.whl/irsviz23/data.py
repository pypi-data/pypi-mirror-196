"""Reads scouting data from the server or from a JSON file.

TODO:
* Put download data function in try-except blocks.
"""

import json
import pathlib
import urllib.request
import urllib.error
import sys

import bokeh.layouts as bklayouts
import bokeh.models as bkmodels
import pandas as pd


DEFAULT_FILE_NAME = "viewer_data.json"
DEFAULT_DATA_PATH = pathlib.Path.cwd()


class ViewerDataError(Exception):
    """Custom exception class for viewer errors."""


class Manager:
    def __init__(self, data_path=None, ip_address=None):
        self.ip_address = ip_address
        if data_path is None:
            self.data_path = DEFAULT_DATA_PATH / DEFAULT_FILE_NAME
        else:
            self.data_path = data_path
        self.data = None

    def load_json_from_file(self):
        if self.data_path.exists():
            with open(self.data_path, "r") as jfile:
                scouting_data =  json.load(jfile)
            return scouting_data
        else:
            return None

    def download_json_data(self):
        if self.ip_address is None:
            return None
        url = f"http://{self.ip_address}:8131/viewerdata"
        print("Downloading data from", url)
        json_data = urllib.request.urlopen(url).read().decode("utf-8")
        print(f"Downloaded {len(json_data)} characters of JSON data.")
        print("Scouting data saved to", self.data_path)
        return json_data

    @staticmethod
    def json_to_df(jdata):
        """Converts JSON string from Flask server into dict of DataFrames
        
        Args: jdata can be a JSON string, or a Python data strcuture created
            by json.load() or json.loads().

        Returns: A dictionary of four pandas DataFrames
        """

        if isinstance(jdata, str):
            jdata = json.loads(jdata)
        table_names = ["measures", "matches", "status", 
                       "teams", "qualitative", "rankingpoints"]
        tables = {}
        for table in table_names:
            if table in jdata:
                tables[table] = pd.DataFrame(jdata[table])
            else: 
                print("WARNING:", table, "table not found in data.")
        return tables
    
    def save_json_data(self, json_data, output_path=None):
        data_path = self.data_path if output_path is None else output_path
        with open(data_path, "w") as jfile:
            jfile.write(json_data)
      
    def get_data(self):
        """Creates or returns tuple of dataframes."""
        if self.data is not None:
            return self.data
        viewer_data = self.load_json_from_file()
        if viewer_data is None:
            viewer_data = self.download_json_data()
            self.save_json_data(viewer_data)
        if viewer_data is None:
            raise ViewerDataError("Unable to load data.")
        else:
            self.data = self.json_to_df(viewer_data)
        return self.data


class RefreshData:
    def __init__(self, graphlist, data_manager):
        self.graphlist = graphlist
        self.data_manager = data_manager

    def refresh_graphs(self):
        json_data = self.data_manager.download_json_data()
        self.data_manager.save_json_data(json_data)
        for graph in self.graphlist:
            try:
                graph.refresh()
            except BaseException as err:
                print(err)

    def get_layout(self):
        divtext = """
        <h2>To Refresh Scouting Data ...</h2>
        <ol>
        <li>Connect to the network that is running the scouting server.</li>
        <li>Press the <i>Refresh from Server</i> button below.</li>
        </ol>
        """
        divwidget = bkmodels.Div(text=divtext)
        btn = bkmodels.Button(label="Refresh from Server", button_type="primary")
        btn.on_click(self.refresh_graphs)
        layout = bklayouts.column(divwidget, btn)
        return layout