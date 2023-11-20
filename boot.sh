#!/bin/bash
source venv/bin/activate

alembic upgrade head
exec uvicorn --host 0.0.0.0 --port 8000 app.main:app 

