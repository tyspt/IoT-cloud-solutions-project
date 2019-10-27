from datetime import datetime
from elasticsearch import Elasticsearch
es = Elasticsearch()

while True:
    res = es.search(index="pressure_test", body={\
    "size":1, "sort": { "time": "desc"},\
        "query": {"match_all": {}}})

    print("Got %d Hits:" % res['hits']['total']['value'])
    for hit in res['hits']['hits']:
        print("%(time)s %(pressure)s" % hit["_source"])
