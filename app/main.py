from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from routes import router
from dataframe import data
from dashboard import dashboard
from kpi import kpi     
from apply_label import label_router
from models import Base
from db import engine
from middleware import middleware_router 
from llm_routes import LLMrouter
from whatsapp import message
import os
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)


app.include_router(dashboard)
app.include_router(middleware_router)
app.include_router(message)
app.include_router(LLMrouter)
