from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from user import router as user_router

app = FastAPI(title="EventPlanner Backend")

# allow frontend (Angular dev server) to call the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:4200",
        "http://127.0.0.1:4200",
    ],
    allow_credentials=True,
    allow_methods=["*"],      # important: lets OPTIONS pass
    allow_headers=["*"],
)

# include our user controller routes (/auth/register, /auth/login)
app.include_router(user_router)

@app.get("/")
def health():
    return {"status": "ok"}

# uvicorn main:app --reload
