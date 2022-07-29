from fastapi import FastAPI
from router import get_page, user,auth

app =FastAPI()

app.include_router(user.router)
app.include_router(auth.router)
app.include_router(get_page.router)

@app.get('/')
def root():
    return {"message":"welcome to my api"}