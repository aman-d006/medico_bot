from logger import logger
import re

def clean_response_text(text):
    """Remove HTML tags and clean up the response text"""
    if not isinstance(text, str):
        return text
    
    # Remove ALL HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    
    # Fix any remaining issues
    text = re.sub(r'\s+', ' ', text)  # Replace multiple spaces with single space
    text = re.sub(r'\n\s*\n', '\n\n', text)  # Normalize newlines
    text = text.strip()
    
    return text

def query_chain(chain, user_input: str):
    try:
        logger.debug(f"Received user query: {user_input}")

        # Invoke the runnable/chain using its available API
        if hasattr(chain, "invoke"):
            result = chain.invoke({"query": user_input})
        elif hasattr(chain, "run"):
            result = chain.run({"query": user_input})
        else:
            result = chain({"query": user_input})

        # Extract response text
        resp_text = None
        sources = []

        if hasattr(result, 'content'):
            resp_text = result.content
        elif isinstance(result, dict):
            resp_text = result.get("content") or result.get("result") or result.get("response") or result.get("text") or ""
            
            # Extract sources
            srcs = result.get("source_documents") or result.get("sources") or []
            for doc in srcs:
                if hasattr(doc, "metadata"):
                    source = doc.metadata.get("source") or doc.metadata.get("sources") or ""
                    if source:
                        sources.append(source)
        elif isinstance(result, str):
            resp_text = result
        else:
            resp_text = str(result)

        # CRITICAL: Clean the response text to remove HTML tags
        if resp_text and isinstance(resp_text, str):
            # First, try to extract just the content if it's wrapped in HTML
            # This handles cases where the entire response is HTML
            html_content_match = re.search(r'<div[^>]*>(.*?)</div>', resp_text, re.DOTALL)
            if html_content_match:
                resp_text = html_content_match.group(1)
            
            # Then remove any remaining HTML tags
            resp_text = clean_response_text(resp_text)
            
            # Specifically target the problematic div tags
            resp_text = resp_text.replace('</div>', '').replace('<div>', '')
            resp_text = resp_text.replace('</div', '').replace('<div', '')
            
            # Final cleanup
            resp_text = resp_text.strip()

        response = {"response": resp_text, "sources": list(set(sources))}  # Remove duplicate sources
        logger.debug(f"Generated response: {response}")
        return response
    except Exception as e:
        logger.exception(f"Error processing query: {e}")
        raise