import os, os.path
import io
from whoosh import index
from whoosh.filedb.filestore import FileStorage
from whoosh.fields import Schema, TEXT, KEYWORD, ID, STORED

if not os.path.exists("indexdir"):
  os.mkdir("indexdir")

storage = FileStorage("indexdir")

schema = Schema(interpret=TEXT(stored=True),
                title=TEXT(stored=True))
                
"""ix = storage.create_index(schema)

writer = ix.writer()
with io.open("songs.csv", "r", encoding = "utf-8") as f:
  for line in f:
    parts = line.split(";")
    writer.add_document(interpret=unicode(parts[0].strip()), 
                        title=unicode(parts[1].strip()))
    
writer.commit()"""

ix = storage.open_index()

from whoosh.qparser import QueryParser
with ix.searcher() as searcher:
    qp = QueryParser("title", schema=ix.schema)
    qp2 = QueryParser("interpret", schema=ix.schema)
    
    qtext = u"dog"
    q = qp.parse(qtext)
    q2 = qp2.parse(qtext)

    results = searcher.search(q, limit=10)
    results.extend(searcher.search(q2, limit=10))
    print results[:5]