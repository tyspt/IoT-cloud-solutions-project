from datetime import datetime
from elasticsearch import Elasticsearch
es = Elasticsearch()

doc = {
    'temperature': 17,
    'time': datetime.now()
}
# insert
res = es.index(index="temp", doc_type='_doc', id=4, body=doc)
print(res['result'])

# get
# res = es.get(index="test-index", doc_type='tweet', id=1)
# print(res['_source'])

# search
res = es.search(index="temp", body={"query": {"match_all": {}}})
print(res)
print("Got %d Hits" % res['hits']['total']['value'])


# res = es.count(index="temp", doc_type='_doc')
# print(res)
