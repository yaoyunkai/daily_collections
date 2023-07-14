"""


Created at 2023/7/14
"""
from fastapi import FastAPI

from .inventory_audit import router as inventory_audit_router

app = FastAPI()

app.include_router(
    inventory_audit_router
)

if __name__ == '__main__':
    # uvicorn.run(app)
    pass
