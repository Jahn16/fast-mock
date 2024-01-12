from pydantic import HttpUrl
from sqlalchemy.orm import Session

from app.models.url import URL


def get_url_by_id(db: Session, id: str) -> URL | None:
    return db.query(URL).get(id)


def get_url(db: Session, url: HttpUrl, user_id: int) -> URL | None:
    return (
        db.query(URL)
        .filter(URL.owner_id == user_id, URL.hostname == url.host)
        .first()
    )


def create_url(db: Session, url: HttpUrl, user_id: int) -> URL:
    db_url = URL(hostname=url.host, owner_id=user_id)
    db.add(db_url)
    db.commit()
    db.refresh(db_url)
    return db_url
