import os
import pandas as pd
from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

df = pd.read_csv("Data_set\\support_tickets.csv")

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    groq_api_key=os.getenv("GROQ_API_KEY")
)

prompt = ChatPromptTemplate.from_template("""
You are a customer support analyst.

Dataset Columns:
{columns}

Sample Data:
{sample_data}

Question:
{question}

Answer based on the dataset.
""")

chain = prompt | llm


def answer_question(question):

    response = chain.invoke(
        {
            "columns": df.columns.tolist(),
            "sample_data": df.head(10).to_string(),
            "question": question
        }
    )

    return response.content