from dataclasses import asdict
from difflib import SequenceMatcher
from .text_alignment import align_passages

def detect_exact_changes(old, new):
    changes=[]; idx=1
    for block in align_passages(old,new):
        tag=block['tag']; op=block['old']; np=block['new']
        if tag=='equal': continue
        if tag=='replace': typ='modified'
        elif tag=='delete': typ='removed'
        else: typ='added'
        old_text='\n'.join(x.text for x in op); new_text='\n'.join(x.text for x in np)
        changes.append({'id':idx,'change_type':typ,'old_text':old_text,'new_text':new_text,
          'old_pages':','.join(str(x.page) for x in op) or '—','new_pages':','.join(str(x.page) for x in np) or '—',
          'old_passage_ids':','.join(str(x.id) for x in op),'new_passage_ids':','.join(str(x.id) for x in np),
          'similarity':None,'category':'General text changes','priority':'Medium','review_status':'Pending','comments':''}); idx+=1
    return changes

def word_diff(old_text,new_text):
    return list(SequenceMatcher(None,old_text.split(),new_text.split()).get_opcodes())
