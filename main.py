from fastapi import FastAPI,Depends
from fastapi.middleware.cors import CORSMiddleware
from user import router as user_router
from core.security import get_current_user_id 
from events import router as event_router

app = FastAPI(title="EventPlanner Backend")


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:4200",
        "http://127.0.0.1:4200",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# include our user controller routes (/auth/register, /auth/login)
app.include_router(user_router)
app.include_router(event_router)

@app.get("/")
def health():
    return {"status": "ok"}

# uvicorn main:app --reload

@app.get("/")
def health():
    return {"status": "ok"}

@app.get("/me")
def read_me(user_id: str = Depends(get_current_user_id)):
    return {"user_id": user_id}