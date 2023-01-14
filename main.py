from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from routers import users
app = FastAPI()
'''
CORS
'''
app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_credentials = True,
    allow_methods= ["*"],
    allow_headers = ["*"]
)

app.include_router(users.router)
