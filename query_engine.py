import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent


load_dotenv()


class QueryEngine:

    def __init__(self, df):

        self.df = df

        self.llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            temperature=0
        )

        self.agent = create_pandas_dataframe_agent(
            llm=self.llm,
            df=self.df,
            verbose=True,
            allow_dangerous_code=True,
            prefix="""
You are a customer support ticket analytics assistant.

The dataframe is named df.

Available columns:
ticket_id
created_at
category
priority
status
response_time_hrs
resolution_time_hrs
agent_id
customer_rating
issue_summary

Valid status values:
Open
Resolved
Escalated

Valid priority values:
Low
Medium
High
Critical

Always use Python pandas operations on df to answer.
Never guess.
Always calculate the answer from the dataframe.
Return concise natural language answers.
""")
    def ask(self, question):

     result = self.agent.invoke(question)

     return result["output"]