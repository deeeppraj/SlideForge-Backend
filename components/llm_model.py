from langchain_groq  import ChatGroq
from dotenv import load_dotenv

load_dotenv()

mymodel = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0.33,
)

mymodel2 = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0.22
)


