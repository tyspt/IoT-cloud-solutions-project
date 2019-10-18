from datetime import datetime
from elasticsearch import Elasticsearch
es = Elasticsearch()

doc = {
    'temperature': 17,
    'time': datetime.now()
}
res = es.index(index="temp", doc_type='_doc', id=4, body=doc)
print(res['result'])
