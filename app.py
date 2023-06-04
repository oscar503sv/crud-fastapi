from fastapi import FastAPI
from routes.user import user

app = FastAPI(
    title="API for users",
    version="0.0.1",
    openapi_tags=[{
        "name": "Users",
        "description": "CRUD routes for users."
    }]
)

app.include_router(user)
