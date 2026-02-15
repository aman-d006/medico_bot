from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

load_dotenv()

# Load Groq config from environment
GROQ_API_KEY=os.getenv("GROQ_API_KEY")
# The model must be provided via the environment. Do not default to an unknown model.
GROQ_MODEL=os.getenv("GROQ_MODEL")

def get_llm_chain(retriever):
    if not GROQ_MODEL:
        raise RuntimeError(
            "GROQ_MODEL is not set. Please set GROQ_MODEL in your .env to a Groq model you have access to,\n"
            "e.g. GROQ_MODEL=groq-<version>. See your Groq console for available models."
        )

    llm=ChatGroq(
        groq_api_key=GROQ_API_KEY,
        model=GROQ_MODEL
    )

    prompt=PromptTemplate(
        input_variables=["context", "query", "question"],
        template="""
        You are **MediBot**, an AI powered assistant trained to help users to understand several medical reports and documents, also answer
        health-related questions.

        Your job is to provide clear, accurate and powerful response based on **provided context** and only if asked provide some legit trusted
        information as per need.

        ---

        **Context**: {context}

        **User Query**: {query}

        **User Question**: {question}

        ---

        **Answer**:
        -EACH SENTENCE MUST BE ON A NEW LINE
        -USE BULLET POINTS FOR LISTS
        - Start a new line after every period
        - Use bullet points (- ) for each statement
        - Keep each line short and readable
        - Add a blank line between sections
        - End with disclaimer on a new line
        -Switch to a new line with each full stop in response.
        -Always provide a response in a clear, calm, rspectful, concise and informative manner.
        -Respond to the user query and question based on the provided context. 
        -Respond in pointwise manner, with each new sentence on a new line,
        -Follow a proper sophisticated response pattern with clean and spacious text ,easy to read.
        -If content is from uploaded document, mention- Information based on uploaded document...
        -Only if the user question is not answerable based on the provided context, 
        provide some legit trusted information as per need and mention in short that following information is not included in document.
        -Do not makeup facts.
        -If given any medical advice or diagnosis, always include a disclaimer that the user 
        should consult with a healthcare professional for personalized medical advice. 
        """
    )
    
    
    def format_docs(docs):
        return "\n\n".join([doc.page_content for doc in docs])
    
    chain = (
        {
            "context": retriever | RunnableLambda(format_docs),
            "query": RunnablePassthrough(),
            "question": RunnablePassthrough()
        }
        | prompt
        | llm
    )
    
    return chain
