from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

load_dotenv()

# Load Groq config from environment
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL")

def get_llm_chain(retriever):
    if not GROQ_MODEL:
        raise RuntimeError(
            "GROQ_MODEL is not set. Please set GROQ_MODEL in your .env to a Groq model you have access to,\n"
            "e.g. GROQ_MODEL=groq-<version>. See your Groq console for available models."
        )

    llm = ChatGroq(
        groq_api_key=GROQ_API_KEY,
        model=GROQ_MODEL,
        temperature=0.2,  # Lower temperature for more consistent responses
    )

    prompt = PromptTemplate(
        input_variables=["context", "query", "question"],
        template="""You are **MediBot**, a professional medical information assistant designed to help users understand medical reports and answer health-related questions with accuracy and empathy.

**Professional Guidelines:**
1. Always prioritize information from the provided context/document
2. Maintain a professional, calm, and respectful tone
3. Be concise yet thorough in explanations
4. Never provide definitive diagnoses or treatment plans
5. Always include appropriate disclaimers for medical advice
6. Acknowledge limitations of AI in medical contexts
7. **NEVER use apologetic language** like "I'm sorry" or "I couldn't find" - instead use professional acknowledgment

---

**Context from Medical Documents**: 
{context}

**User Query**: {query}

**User Question**: {question}

---

**Response Structure:**

**IF RELEVANT INFORMATION IS FOUND IN THE CONTEXT:**
- Provide accurate information based strictly on the context
- Organize information clearly (use bullet points for multiple items)
- Explain medical terms in simple language when needed
- End with a brief summary if appropriate

**IF NO RELEVANT INFORMATION IS FOUND IN THE CONTEXT:**
- Begin with: "The provided documents do not contain specific information about [topic]."
- Then provide general educational information (clearly mark as "**General Information**")
- Format the general information with clear sections:
  - **What it is**: Brief definition
  - **Main types**: If applicable
  - **Common symptoms**: If applicable
  - **Risk factors**: If applicable
  - **Management**: If applicable
- End with: "**What documents might contain more detailed information?**"
- Suggest document types that would contain this information

**ALWAYS INCLUDE THIS DISCLAIMER** at the end of your response:
**IMPORTANT**: This information is for educational purposes only and is not a substitute for professional medical advice, diagnosis, or treatment. Always seek the advice of your physician or other qualified health provider with any questions you may have regarding a medical condition.

---

**Answer**:"""
    )
    
    def format_docs(docs):
        """Format retrieved documents with source tracking"""
        if not docs:
            return "No relevant documents were found in the database for this query."
        
        formatted_docs = []
        for i, doc in enumerate(docs, 1):
            source = doc.metadata.get('source', 'Unknown source')
            content = doc.page_content
            formatted_docs.append(f"[Document {i} - Source: {source}]\n{content}")
        
        return "\n\n".join(formatted_docs)
    
    def check_document_relevance(inputs):
        """Check if documents were found and route appropriately"""
        context = inputs.get("context", "")
        query = inputs.get("query", "")
        question = inputs.get("question", "")
        
        # Extract the main topic from the question for better responses
        topic = question if question else query
        
        # If no context or context indicates no documents
        if not context or "No relevant documents were found" in context:
            return {
                "context": context,
                "query": query,
                "question": question,
                "topic": topic,
                "has_documents": False
            }
        return {
            "context": context,
            "query": query,
            "question": question,
            "topic": topic,
            "has_documents": True
        }
    
    # Create the chain
    chain = (
        {
            "context": retriever | RunnableLambda(format_docs),
            "query": RunnablePassthrough(),
            "question": RunnablePassthrough()
        }
        | RunnableLambda(check_document_relevance)
        | prompt
        | llm
    )
    
    return chain