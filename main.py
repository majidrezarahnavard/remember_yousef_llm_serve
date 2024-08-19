from faqs import FAQs
from typing import Union
from pydantic import BaseModel
from fastapi import FastAPI
from dotenv import load_dotenv

load_dotenv(".env")

app = FastAPI()
faqs = FAQs()

class Message(BaseModel):
    text: str
    
class MessageModel(BaseModel):
    text: str
    fine_tuned_model : str


@app.post("/api/v1/ask")
def ask(message: Message):
    response = faqs.request(message.text)
    return {"message": response }
