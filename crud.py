from sqlalchemy.orm import Session
import models

def create_chat_message(db: Session, role: str, text: str, user_id: int):
    db_message = models.ChatMessage(role=role, text=text, user_id=user_id)
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message


def get_conversation_history(db: Session, user_id: int, limit: int = 20):
    messages = db.query(models.ChatMessage).filter(models.ChatMessage.user_id == user_id).order_by(models.ChatMessage.timestamp.asc()).limit(limit).all()
    system_prompt = [{"role": "system", "content": "You are a helpful photo mentor chatbot dedicated to discuss capture ideas, techniques, location scouting and any thing related to photography. You can also assist in developing portfolios, project proposals, blog posts and many other things." }]
    # Format the messages as desired
    history = [{"role": message.role, "content": message.text} for message in messages]
    return system_prompt + history