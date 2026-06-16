import os
from dotenv import load_dotenv
import pandas as pd
from groq import Groq
load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

df = pd.read_csv("support_tickets.csv")

def answer_question(question):

    prompt = f"""
You are analyzing a customer support dataset.

Columns:
{list(df.columns)}

Sample Data:
{df.head(10).to_string()}

Question:
{question}

Answer based on the dataset.
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0
    )

    return response.choices[0].message.content