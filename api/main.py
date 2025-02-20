
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
API_KEY =os.getenv("OPENROUTER_API_KEY")
print("api key=",API_KEY)


# Initialize LangChain Chat Model using OpenRouter
chat_model = ChatOpenAI(model="mistralai/mistral-small-24b-instruct-2501:free",openai_api_key=API_KEY,openai_api_base="https://openrouter.ai/api/v1")

# Event Rules and Regulations
EVENT_RULES = """
**ThinkQuest-2K25 | 3rd March 2025**  

## UG Events:  
- **Ad-Zap**: (2-3/team) Topics on the spot, own props allowed.  
- **Dumb Charades**: (2/team) Topics on the spot, one acts, others guess.  
- **Quiz**: Solo event, programming & computer technology.  

## PG Events:  
- **Short Film**: (2/team) 5-10 min, topics: Tech vs Life, Error 404, Digital Trap, Virtual Life, Algorithm of Life. Content in pendrive/laptop.  
- **Web Design**: Solo event, HTML, CSS, JS.  
- **VizSpark**: Solo event, tools: Power BI, Tableau, Excel. Time limit: 1 hour, dataset provided on the spot.  

## Registration:  
- **Fee**: ₹150 per participant  
- **Form Link**: [Google Form](https://docs.google.com/forms/d/e/1FAIpQLSfylNlEUBPjGjJcP-AWYJolosYwXN5lbkZ7DgwXb1ab1yVdvhA/viewform?usp=sf_link)  
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

## Student Committee Members:  
V. RameshKumar, R. BalaMurugan, S. NireshKumar, M. Farvash Musraf, R. Bhuvana, T. Udhayanithi, A. Siva, S. Jagathesan, D. Kabilan, P. Devika  

## Contact:  
- **T. Udhayanithi**: 9597540931  
- **R. BalaMurugan**: 7904765141  
- **V. RameshKumar**: 7010554788  (creater of this website)
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
        SystemMessage(content=f"You are an event assistant for Thinkquest-2K25. Use the following rules: {EVENT_RULES}"),
        HumanMessage(content=user_message)
    ]

    # Generate response
    response = chat_model.invoke(messages)
    print("response ldllldld : ",response)

    return {"response": response.content}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)