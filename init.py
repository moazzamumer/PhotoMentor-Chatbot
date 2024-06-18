from fastapi import FastAPI, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import uvicorn, os
import db_conn, models, crud, gpt

load_dotenv()
PORT = int(os.getenv("PORT"))
HOST = os.getenv("HOST")


engine, SessionLocal = db_conn.create_db()
models.Base.metadata.create_all(bind=engine)

app = FastAPI()
user_sessions = {}


origins = [
    "*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
)


# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/chat")
async def chat(user_id: int, prompt: str, db: Session = Depends(get_db)):

    if user_id not in user_sessions:
        user_sessions[user_id] = gpt.GPT()
    
    # Store the user's message in the database
    crud.create_chat_message(db, role="user", text=prompt, user_id=user_id)

    history = crud.get_conversation_history(db, user_id)

    #print(history)

    # Generate a response using the GPT API
    gpt_call = user_sessions[user_id]

    #return {"assistant_message": assistant_message.text}
    return StreamingResponse(gpt_call.get_response(history, user_id, db), media_type='text/plain')


if __name__ == "__main__":
    
    uvicorn.run("init:app", host = HOST, port = PORT, reload = True)