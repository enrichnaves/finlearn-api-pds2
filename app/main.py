from fastapi import Depends, FastAPI
from sqlalchemy import select
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from app.core.middleware.db import get_db
from app.api.v1.api import api_router as router_v1

app = FastAPI(title="Finlearn")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router_v1, prefix="/v1")


@app.get("/")
def healthcheck(db: Session = Depends(get_db)):
    db.execute(select(1))
    return {"status": True}
