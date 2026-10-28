from .database import Database
def update_review(db: Database, change_id:int, status:str, comments:str=''): db.update_review(change_id,status,comments)
