from manonaid_helpers.download import Download
from manonaid_helpers.utils import Utils

LISTOFFILES = ["9400409_empty.csv"]
FOLDER = "predictions/2022-12-11/"

list_blobs = Utils(container="cyi5", name_starts_with=FOLDER).list_blobs()


df = Download(
    source="cyi5", folder="MR-spire2-sql/", delimitter="\t", list_files=["7221275.csv"]
).returnAsDataFrameDict()
