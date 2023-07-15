"""


Created at 2023/7/14
"""
from fastapi import FastAPI

from .attendance import views
from .database import Base
from .database import engine

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(
    views.router,
    prefix='/attendance'
)

if __name__ == '__main__':
    # uvicorn.run(app)
    pass
