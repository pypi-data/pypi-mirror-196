from irsviz23 import data
import pathlib
import json

import pytest

# def test_server_data():
#     print(data.get_data_from_server())

# def test_get_data():
#     assert len(data.get_data()) == 4
OUTPUT_PATH = pathlib.Path(__file__).parent / "outputs"
INPUT_PATH = pathlib.Path(__file__).parent / "inputs"
INPUT_FILE = INPUT_PATH / "pytest_viewer_data.json"

@pytest.fixture
def json_data():
    with open(INPUT_FILE, "r") as jfile:
        return json.load(jfile)

@pytest.fixture
def empty_outputs():
    for file in OUTPUT_PATH.iterdir():
        file.unlink()
    return True

@pytest.fixture
def manager():
    return data.Manager(data_path=INPUT_FILE, ip_address="127.0.0.1")

def test_load_data_file(manager):
    scouting_data = manager.load_json_from_file()
    assert isinstance(scouting_data, dict)
    tables = ["measures", "matches", "status", "teams", "qualitative", "rankingpoints"]
    for key in tables:
        assert key in scouting_data.keys()
    assert len(scouting_data) == len(tables)


def test_download(manager, empty_outputs):
    """Test requires scouting server to be running."""
    json_data = manager.download_json_data()
    assert isinstance(json_data, str)
    assert len(json_data) > 400_000
    manager.save_json_data(json_data)


def test_data_conversion(json_data, manager):
    df = manager.json_to_df(json_data)
    keys = json_data.keys()
    assert len(df.keys()) == 6
    for key in ['matches', 'measures', 'status', 'teams', 'qualitative', 'rankingpoints']:
        assert key in keys
        print(df[key].shape)
    assert df['status'].shape == (2, 2)
    assert df['matches'].shape[1] == 4
    assert df['matches'].shape[0] > 100
    assert df['measures'].shape[1] == 8
    assert df['measures'].shape[0] > 100
    assert df['teams'].shape[1] == 5
    assert df['teams'].shape[0] > 30
    assert df['qualitative'].shape == (2, 2)
    assert df["rankingpoints"].shape == (2, 2)

def test_save(json_data, empty_outputs, manager):
    assert empty_outputs
    file_path = OUTPUT_PATH / "pytest_viewer_data.json"
    json_str = json.dumps(json_data)
    manager.save_json_data(json_str, file_path)
    with open(file_path, "r") as jfile:
        loaded_data = json.load(jfile)
    keys = loaded_data.keys()
    for key in ['matches', 'measures', 'status', 'teams', 'qualitative', 'rankingpoints']:
        assert key in keys
