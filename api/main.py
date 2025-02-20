
import uvicorn
from langchain.schema import SystemMessage, HumanMessage
import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain_openai import ChatOpenAI

load_dotenv()
from fastapi.middleware.cors import CORSMiddleware


# Initialize FastAPI app
app = FastAPI()
# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change "*" to specific domains in production
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods including OPTIONS
    allow_headers=["*"],  # Allows all headers
)
# Load OpenRouter API key
API_KEY ="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"
print("api key=",API_KEY)


# Initialize LangChain Chat Model using OpenRouter
chat_model = ChatOpenAI(model="qwen/qwen2.5-vl-72b-instruct:free",openai_api_key=API_KEY,openai_api_base="https://openrouter.ai/api/v1")

# Event Rules and Regulations
EVENT_RULES = """
1. Coding Contest: Participants must register before 10 AM.
2. Hackathon: Team size should be 2-4 members. Submission by 5 PM.
3. Paper Presentation: Slides must be submitted by 2 PM.
4. Treasure Hunt: Teams must check in at the auditorium by 11 AM.
"""

# Define a sample route
@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI on Google Colab"}
# Request model
class ChatRequest(BaseModel):
    message: str

# Response model
class ChatResponse(BaseModel):
    response: str
@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    user_message = request.message.strip()

    if not user_message:
        raise HTTPException(status_code=400, detail="Message is required")

    # Structure messages for LangChain
    messages = [
        SystemMessage(content=f"You are an event assistant for OPTRA-2K25. Use the following rules: {EVENT_RULES}"),
        HumanMessage(content=user_message)
    ]

    # Generate response
    response = chat_model.invoke(messages)
    #response = chat_model(messages)
    print("response ldllldld : ",response)

    return {"response": response.content}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)