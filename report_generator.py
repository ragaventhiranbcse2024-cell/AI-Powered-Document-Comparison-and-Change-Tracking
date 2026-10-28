import csv, io
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

def csv_bytes(changes):
 out=io.StringIO(); fields=['id','change_type','old_text','new_text','old_pages','new_pages','category','priority','similarity','review_status','comments']; w=csv.DictWriter(out,fieldnames=fields); w.writeheader(); w.writerows({k:c.get(k,'') for k in fields} for c in changes); return out.getvalue().encode()
def pdf_bytes(title,changes,summary=''):
 buf=io.BytesIO(); doc=SimpleDocTemplate(buf,pagesize=letter,rightMargin=36,leftMargin=36); styles=getSampleStyleSheet(); story=[Paragraph(title,styles['Title']),Spacer(1,12),Paragraph(summary.replace('&','&amp;').replace('\n','<br/>'),styles['BodyText']),Spacer(1,12)]
 for c in changes: story += [Paragraph(f"Change {c.get('id')}: {c.get('change_type')} | {c.get('category')} | {c.get('priority')} | old page {c.get('old_pages')} / new page {c.get('new_pages')}",styles['Heading4']),Paragraph(f"Old: {c.get('old_text') or '—'}<br/>New: {c.get('new_text') or '—'}<br/>Review: {c.get('review_status')} | Comments: {c.get('comments') or '—'}",styles['BodyText']),Spacer(1,8)]
 doc.build(story); return buf.getvalue()
