import pandas as pd
from sklearn.cluster import DBSCAN
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
from adtk.detector import MinClusterDetector
from sklearn.cluster import Birch
from adtk.visualization import plot
import os 

token = os.environ.get('TOKEN')
org = os.environ.get('ORGANIZATION')

pointname = "X_Analytics"
bucket = "bucket"

client = InfluxDBClient(url="http://localhost:8086", token=token, org=org)
query = '''from(bucket: "''' + bucket + '''")
  |> range(start: -100h)
  |> filter(fn: (r) => r["_measurement"] == "sps")
  |> filter(fn: (r) => r["_field"] == "128U3EL3162Channel2Value")
  |> aggregateWindow(every: 1s, fn: mean, createEmpty: false)
  |> yield(name: "mean")'''

 
query_api = client.query_api()
df = query_api.query_data_frame(query)

df["_time"] = pd.to_datetime(df["_time"].astype(str))
df = df.drop(columns=["result", "table","_start", "_stop", "_measurement","_field", "host", "topic"])
df = df.set_index("_time")


min_cluster_detector = MinClusterDetector(Birch(n_clusters=10))
anomalies = min_cluster_detector.fit_detect(df)

write_api = client.write_api(write_options=SYNCHRONOUS)
for element in range(anomalies.size):
  point = Point(pointname).field("anomaly", df["_value"][element]).time(df.index[element], WritePrecision.NS).tag("isAnomaly", anomalies[element])
  write_api.write(bucket, org, point)
