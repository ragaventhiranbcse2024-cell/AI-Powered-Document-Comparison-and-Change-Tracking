import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parents[1]))
from modules.exact_diff import detect_exact_changes
from modules.semantic_analysis import semantic_changes
from modules.change_classifier import classify_changes
from modules.database import Database
from modules.report_generator import csv_bytes,pdf_bytes
from modules.text_extractor import Passage

def test_added_removed_modified():
 old=[Passage(1,1,'Alpha policy applies.'),Passage(2,2,'Pay 10 days.')]
 new=[Passage(1,1,'Alpha policy applies.'),Passage(2,2,'Pay 20 days.'),Passage(3,3,'New clause.')]
 ch=classify_changes(semantic_changes(detect_exact_changes(old,new),.7))
 assert any(x['change_type']=='modified' for x in ch); assert len(ch)>=1
 assert any(x.get('number_change') for x in ch)
def test_database_review(tmp_path):
 db=Database(tmp_path/'x.sqlite'); did=db.add_document('x'); a=db.add_version(did,'a','2026-01-01','',tmp_path/'a'); b=db.add_version(did,'b','2026-01-02','',tmp_path/'b'); cid=db.add_comparison(a,b,[{'change_type':'added','old_text':'','new_text':'x','old_pages':'—','new_pages':'1','category':'General','priority':'Low','similarity':None}]); rows=db.list_changes(cid); assert len(rows)==1; db.update_review(rows[0]['id'],'Accepted','ok'); assert db.list_changes(cid)[0]['review_status']=='Accepted'
def test_exports():
 c=[{'id':1,'change_type':'added','old_text':'','new_text':'x','old_pages':'—','new_pages':'1','category':'General','priority':'Low','similarity':None,'review_status':'Pending','comments':''}]
 assert b'new_text' in csv_bytes(c); assert pdf_bytes('R',c,'summary').startswith(b'%PDF')
