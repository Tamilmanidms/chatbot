
import uvicorn
from langchain.schema import SystemMessage, HumanMessage
import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
<<<<<<< HEAD
from langchain_openai.chat_models import ChatOpenAI

=======
from langchain_openai import ChatOpenAI

load_dotenv()
>>>>>>> 905c0775afb684fd1d87cd1fb375f072a3c8c166
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
API_KEY =os.getenv("OPENROUTER_API_KEY")


# Initialize LangChain Chat Model using OpenRouter
chat_model = ChatOpenAI(model="mistralai/mistral-7b-instruct:free",openai_api_key=API_KEY,openai_api_base="https://openrouter.ai/api/v1",max_tokens=250)

# Event Rules and Regulations
EVENT_RULES = """
**ThinkQuest-2K25 | 3rd March 2025**  

## UG Events:  
- **Ad-Zap**: (2-3/team) Topics on the spot, own props allowed.  
- **Dumb Charades**: (2/team) Topics on the spot, one acts, others guess.  
- **Quiz**: Solo event, programming & computer technology.  

## PG Events:  
- **Short Film**: (2/team) 5-10 min, topics: Tech vs Life, Error 404, Digital Trap, Virtual Life. Content in pendrive/laptop.  
- **Web Design**: Solo event, HTML, CSS, JS.  
- **VizSpark**: Solo event, tools: Power BI, Tableau, Excel. Time limit: 1 hour, dataset provided on the spot.  

## Registration:  
- **Fee**: ₹150 per participant  
- **Form Link**: [Google Form](https://docs.google.com/forms/d/e/1FAIpQLScQbNUps4ZjFJS20xnHrmBmtFSCfKUA_p6ygzuiBdazKs7cSQ/viewform)  
- **Chatbot**: [thinkquest-2k25.web.app](https://thinkquest-2k25.web.app)  
- **Website**: [nmc.ac.in](https://www.nmc.ac.in)  

## About the College:  
Nehru Memorial College (NMC), Puthanampatti, Tamil Nadu. Established in 1967, affiliated with Bharathidasan University, accredited 'A+' by NAAC.  

## Organizing Committee:  
- **President**: Thiru. Pon. Balasubramanian  
- **Secretary**: Thiru. Pon. Ravichandran  
- **Principal**: Dr. A. Venkatesan  
- **Vice-Principal**: Dr. K.T. Tamilmani  
- **Coordinator**: Dr. M. Meenakshi Sundaram  
- **Convenors**: Dr. V. Umadevi, Dr. S. Mala, Dr. V. Priya  
- **Chief Guest**: Madhuprasad R (General Manager)  

## Student Committee Members:  
V. RameshKumar, R. BalaMurugan, S. NireshKumar, M. Farvash Musraf, R. Bhuvana, T. Udhayanithi, A. Siva, S. Jagathesan, D. Kabilan, P. Devika  

## Contact incharges or organizing members:  
- **T. Udhayanithi**: 9597540931  
- **R. BalaMurugan**: 7904765141  
- **V. RameshKumar**: 7010554788  

## Creator of this chatbot and Website:  
- **V. Rameshkumar**: [LinkedIn](https://www.linkedin.com/in/rameshkumar-v)  
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

    system_prompt = (
        "You are a chatbot assistant for ThinkQuest-2K25, an event happening on 3rd March 2025."
        " Answer queries accurately using the event details below. Keep responses short and relevant."
        " If unsure, ask for clarification instead of guessing."
    )

    # Structure messages for LangChain
    messages = [
        SystemMessage(content=system_prompt),
        SystemMessage(content=EVENT_RULES),
        HumanMessage(content=user_message),
    ]

    # Generate response
    response = chat_model.invoke(messages)
    print("response ldllldld : ",response)

    return {"response": response.content}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)