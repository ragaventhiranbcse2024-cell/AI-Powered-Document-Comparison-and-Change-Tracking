from difflib import SequenceMatcher
from .text_extractor import Passage

def align_passages(old: list[Passage], new: list[Passage]):
    sm=SequenceMatcher(None,[p.text for p in old],[p.text for p in new],autojunk=False)
    result=[]
    for tag,i1,i2,j1,j2 in sm.get_opcodes(): result.append({'tag':tag,'old':old[i1:i2],'new':new[j1:j2]})
    return result
