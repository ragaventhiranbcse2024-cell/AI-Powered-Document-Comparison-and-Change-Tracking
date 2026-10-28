import os, re, math

def _tokens(s): return set(re.findall(r'[a-zA-Z0-9]+', s.lower()))
def lexical_similarity(a,b):
    x,y=_tokens(a),_tokens(b)
    return len(x&y)/math.sqrt(len(x)*len(y)) if x and y else 0.0

def embedding_similarity(a, b):
    """Calculate cosine similarity with Sentence Transformers when enabled."""
    from sentence_transformers import SentenceTransformer
    model = SentenceTransformer(os.getenv('SEMANTIC_MODEL', 'all-MiniLM-L6-v2'))
    vectors = model.encode([a, b], normalize_embeddings=True)
    return float(vectors[0] @ vectors[1])

def semantic_changes(changes, threshold=.72):
    for c in changes:
        if c['old_text'] and c['new_text']:
            if os.getenv('USE_SENTENCE_TRANSFORMERS', '').lower() in {'1', 'true', 'yes'}:
                try: c['similarity'] = round(embedding_similarity(c['old_text'], c['new_text']), 3)
                except Exception: c['similarity'] = round(lexical_similarity(c['old_text'],c['new_text']),3)
            else: c['similarity'] = round(lexical_similarity(c['old_text'],c['new_text']),3)
            nums_old=set(re.findall(r'\b\d+(?:[.,]\d+)?%?\b',c['old_text'])); nums_new=set(re.findall(r'\b\d+(?:[.,]\d+)?%?\b',c['new_text']))
            c['semantic_flag']=c['similarity'] >= threshold and c['old_text'].strip()!=c['new_text'].strip()
            c['number_change']=nums_old != nums_new
            if c['number_change']: c['category']='Numerical or date changes'; c['priority']='High'
            elif c['semantic_flag']: c['category']='Potential meaning change'
        else: c['semantic_flag']=False; c['number_change']=False
    return changes
