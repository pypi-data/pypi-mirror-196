from manonaid_helpers.download import Download

df = Download(
    source="cyi5", folder="predictions/2022-12-11/", list_files=["9400409_empty.csv"]
).returnAsDataFrameDict()
