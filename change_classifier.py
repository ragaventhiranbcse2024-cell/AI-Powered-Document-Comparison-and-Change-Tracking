import re

def classify_changes(changes):
    for c in changes:
        text=(c.get('old_text','')+' '+c.get('new_text','')).lower()
        if c.get('number_change') or re.search(r'\b(date|deadline|year|month|%|amount|days?)\b',text): c['category']='Numerical or date changes'; c['priority']='High'
        elif re.search(r'\b(must|required|shall|responsible|obligation|prohibited)\b',text): c['category']='Obligation or responsibility changes'; c['priority']='High'
        elif re.search(r'\b(policy|compliance|procedure)\b',text): c['category']='Policy changes'; c['priority']='Medium'
        elif c['change_type']=='modified': c['category']='General text changes'; c['priority']='Medium'
        else: c['category']='Formatting or structural changes'; c['priority']='Low'
    return changes
