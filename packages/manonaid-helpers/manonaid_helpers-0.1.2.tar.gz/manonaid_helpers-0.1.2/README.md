
# Installation

```commandline
pip install manonaid_helpers
```

See [PyPi](https://pypi.org/project/manonaid-helpers/) for package index.

# Requirements

Azure Storage connection string has to be set as environment variable `AZURE_STORAGE_CONNECTION_STRING` or
the seperate environment variables `AZURE_STORAGE_KEY` and `AZURE_STORAGE_NAME` which will be used to create the connection string.

# Usage

## Download

### 1. Fetch as pd.DataFrame

We can use the `returnAsDataFrameDict()` method to fetch one or multiple blobs as DataFrames

If we fetch only one blob it is returned as a DataFrame

While fetching multiple blobs the return object is a dictonary of DataFrames with the blob name(with the extension) as the key.

For all blobs that contain columns with names containing "date" or "time" are converted to datetime with format="%Y-%m-%dT%H:%M:%S" 

```python
from manonaid_helpers.download import Download

df = Download(
    source="cyi5", 
    extension=".csv", 
    folder="pack_test/"
).returnAsDataFrameDict()

```

### 2. Download a specific folder from a container

We can download a folder by setting the `folder` argument.

```python
from manonaid_helpers.download import Download

Download(
   source='cyi5',
   folder="pack_test/",
   extension='.csv',
).returnAsDataFrameDict()
```

### 3. Download a given list of files

We can give a list of files to download with the `list_files` argument.

```python
from manonaid_helpers.download import Download

Download(
   source='cyi5',
   folder="pack_test/",
   extension='.csv',
   list_files=["20230301_ais_accuracy.csv"],
).returnAsDataFrameDict()
```
