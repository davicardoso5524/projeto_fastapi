from fastapi import FastAPI

app = FastAPI()

from routes.auth_routes import auth_router
from routes.orders_routes import order_router

app.include_router(auth_router)
app.include_router(order_router)