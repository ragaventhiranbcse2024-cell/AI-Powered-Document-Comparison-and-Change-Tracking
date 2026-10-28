import sqlite3
from datetime import datetime, timezone
from pathlib import Path

def now(): return datetime.now(timezone.utc).isoformat()
class Database:
 def __init__(self,path): self.path=str(path); self.init()
 def conn(self): c=sqlite3.connect(self.path); c.row_factory=sqlite3.Row; return c
 def init(self):
  with self.conn() as c:
   c.executescript('''CREATE TABLE IF NOT EXISTS documents(id INTEGER PRIMARY KEY, name TEXT, created_at TEXT); CREATE TABLE IF NOT EXISTS versions(id INTEGER PRIMARY KEY, document_id INTEGER, name TEXT, version_date TEXT, description TEXT, path TEXT, created_at TEXT, FOREIGN KEY(document_id) REFERENCES documents(id)); CREATE TABLE IF NOT EXISTS comparisons(id INTEGER PRIMARY KEY, old_version_id INTEGER, new_version_id INTEGER, created_at TEXT); CREATE TABLE IF NOT EXISTS changes(id INTEGER PRIMARY KEY, comparison_id INTEGER, change_type TEXT, old_text TEXT, new_text TEXT, old_pages TEXT, new_pages TEXT, category TEXT, priority TEXT, similarity REAL, review_status TEXT DEFAULT "Pending", comments TEXT DEFAULT "", created_at TEXT); CREATE TABLE IF NOT EXISTS audit_events(id INTEGER PRIMARY KEY, change_id INTEGER, action TEXT, details TEXT, created_at TEXT)''')
 def add_document(self,name):
  with self.conn() as c: return c.execute('INSERT INTO documents(name,created_at) VALUES(?,?)',(name,now())).lastrowid
 def add_version(self,doc_id,name,date,desc,path):
  with self.conn() as c: return c.execute('INSERT INTO versions(document_id,name,version_date,description,path,created_at) VALUES(?,?,?,?,?,?)',(doc_id,name,date,desc,str(path),now())).lastrowid
 def add_comparison(self,old_id,new_id,changes):
  with self.conn() as c:
   cid=c.execute('INSERT INTO comparisons(old_version_id,new_version_id,created_at) VALUES(?,?,?)',(old_id,new_id,now())).lastrowid
   for x in changes: c.execute('INSERT INTO changes(comparison_id,change_type,old_text,new_text,old_pages,new_pages,category,priority,similarity,review_status,comments,created_at) VALUES(?,?,?,?,?,?,?,?,?,?,?,?)',(cid,x['change_type'],x['old_text'],x['new_text'],x['old_pages'],x['new_pages'],x.get('category'),x.get('priority'),x.get('similarity'),x.get('review_status','Pending'),x.get('comments',''),now()))
   return cid
 def list_changes(self,cid):
  with self.conn() as c:return [dict(x) for x in c.execute('SELECT * FROM changes WHERE comparison_id=? ORDER BY id',(cid,))]
 def update_review(self,change_id,status,comments):
  with self.conn() as c:
   c.execute('UPDATE changes SET review_status=?,comments=? WHERE id=?',(status,comments,change_id)); c.execute('INSERT INTO audit_events(change_id,action,details,created_at) VALUES(?,?,?,?)',(change_id,status,comments,now()))
 def versions(self):
  with self.conn() as c:return [dict(x) for x in c.execute('SELECT v.*,d.name AS document_name FROM versions v JOIN documents d ON d.id=v.document_id ORDER BY v.created_at DESC')]
