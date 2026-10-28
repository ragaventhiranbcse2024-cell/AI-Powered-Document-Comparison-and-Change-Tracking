import streamlit as st
from pathlib import Path
from datetime import date
from config import DB_PATH
from modules.document_loader import save_upload, ValidationError
from modules.text_extractor import extract_pages, ExtractionError
from modules.exact_diff import detect_exact_changes
from modules.semantic_analysis import semantic_changes
from modules.change_classifier import classify_changes
from modules.ai_summary import generate_summary
from modules.database import Database
from modules.report_generator import csv_bytes,pdf_bytes

st.set_page_config(page_title='AI Document Comparison',page_icon='↔',layout='wide')
db=Database(DB_PATH)
st.title('AI-Powered Document Comparison and Change Tracking')
st.caption('Evidence-linked comparison with exact diffs, semantic review suggestions, human review, and exports.')
if 'changes' not in st.session_state: st.session_state.changes=[]
with st.sidebar:
 st.header('Workflow'); page=st.radio('Navigate',['Home','Upload & Compare','Review Changes','Export Reports','Version History','Settings'])
 st.info('Semantic similarity and classifications are suggestions only. Human verification is required for important decisions.')
if page=='Home':
 st.subheader('Dashboard'); ch=st.session_state.changes
 a,b,c,d=st.columns(4); a.metric('Detected changes',len(ch)); b.metric('Added',sum(x['change_type']=='added' for x in ch)); c.metric('Removed',sum(x['change_type']=='removed' for x in ch)); d.metric('High priority',sum(x.get('priority')=='High' for x in ch))
 st.markdown('### Getting started'); st.write('Upload two PDF or DOCX versions, run comparison, inspect source pages, review findings, then export an auditable report.')
elif page=='Upload & Compare':
 st.subheader('Upload and compare document versions'); oldf=st.file_uploader('Older version',type=['pdf','docx'],key='old'); newf=st.file_uploader('Newer version',type=['pdf','docx'],key='new')
 threshold=st.slider('Semantic similarity threshold',0.0,1.0,0.72,0.01)
 if st.button('Run comparison',type='primary'):
  if not oldf or not newf: st.error('Select both versions.'); st.stop()
  try:
   op=save_upload(oldf.name,oldf.getvalue()); np=save_upload(newf.name,newf.getvalue()); old,w1=extract_pages(op); new,w2=extract_pages(np)
   for w in w1+w2: st.warning(w)
   ch=classify_changes(semantic_changes(detect_exact_changes(old,new),threshold)); st.session_state.changes=ch; st.session_state.summary=generate_summary(ch)
   docid=db.add_document(Path(newf.name).stem); oldid=db.add_version(docid,'Older version',str(date.today()),'',op); newid=db.add_version(docid,'Newer version',str(date.today()),'',np); st.session_state.comparison_id=db.add_comparison(oldid,newid,ch)
   st.success(f'Comparison complete: {len(ch)} changes detected.')
  except (ValidationError,ExtractionError) as e: st.error(str(e))
 if st.session_state.changes:
  st.dataframe(st.session_state.changes,use_container_width=True)
elif page=='Review Changes':
 st.subheader('Review and annotate'); ch=st.session_state.changes
 if not ch: st.info('Run a comparison first.'); st.stop()
 for x in ch:
  with st.expander(f"Change {x['id']} · {x['change_type']} · {x.get('priority')} · {x.get('category')}"):
   st.markdown(f"**Old page(s):** {x['old_pages']}  |  **New page(s):** {x['new_pages']}  |  **Similarity:** {x.get('similarity','—')}")
   st.markdown(f"<div style='background:#fee2e2;padding:8px'><b>Old:</b> {x['old_text'] or '—'}</div><div style='background:#dcfce7;padding:8px'><b>New:</b> {x['new_text'] or '—'}</div>",unsafe_allow_html=True)
   status=st.selectbox('Decision',['Pending','Accepted','Dismissed','Further review'],index=['Pending','Accepted','Dismissed','Further review'].index(x.get('review_status','Pending')),key=f's{x["id"]}')
   comment=st.text_area('Reviewer comment',x.get('comments',''),key=f'c{x["id"]}')
   if st.button('Save review',key=f'b{x["id"]}'):
    x['review_status']=status;x['comments']=comment
    if st.session_state.get('comparison_id'): db.update_review(x['id'],status,comment)
    st.success('Review saved.')
elif page=='Export Reports':
 st.subheader('Export reports'); ch=st.session_state.changes
 if not ch: st.info('Run a comparison first.'); st.stop()
 summary=st.session_state.get('summary',generate_summary(ch)); st.text_area('Evidence-based summary',summary,height=220)
 st.download_button('Download CSV',csv_bytes(ch),'comparison_changes.csv','text/csv'); st.download_button('Download PDF',pdf_bytes('Document Comparison Report',ch,summary),'comparison_report.pdf','application/pdf')
elif page=='Version History':
 st.subheader('Version history'); st.dataframe(db.versions(),use_container_width=True)
elif page=='Settings':
 st.subheader('Settings and project information'); st.write('Supported formats: PDF and DOCX. Originals are copied with UUID filenames and never modified. SQLite database:',str(DB_PATH)); st.write('Semantic fallback uses lexical cosine-like overlap when Sentence Transformers is unavailable. Configure API integrations through environment variables; no credentials are hardcoded.')
