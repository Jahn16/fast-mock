from pydantic import HttpUrl
from sqlalchemy.orm import Session

from app.models.url import URL

def get_url_by_id(db: Session, id: str):
    return db.query(URL).get(id)

def get_url(db: Session, url: HttpUrl):
    return db.query(URL).filter(URL.hostname == url.host).first()

def create_url(db: Session, url: HttpUrl):
    db_url = URL(hostname=url.host)
    db.add(db_url)
    db.commit()
    db.refresh(db_url)
    return db_url
