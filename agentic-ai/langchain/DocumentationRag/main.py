from typing import List, Any, Dict

import streamlit as st
from backend.core import run_llm


#pipenv run streamlit run main.py - to run the app

def format_sources(context_docs:List[Any])-> List[str]:
    """Format the retrieved documents for display in the Streamlit app."""
    return [
        str(meta.get("source", "Unknown"))
        for doc in (context_docs or [])
        if (meta := getattr(doc, "metadata", None) or {}) is not None
    ]

st.set_page_config(page_title="Langchain documentation helper", layout="centered")
st.title("Langchain Documentation Helper")

with st.sidebar:
    st.subheader("Session")
    if (st.button("Clear Session", use_container_width=True)):
        st.session_state.pop("messages", None)
        st.rerun()
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role":"Assistant",
         "content":"Ask me anything about langchain docs. I will retrieve relevant context and cite the sources",
         "sources": []
         }
    ]
# this will be how the chat window be
for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if message.get("sources"):
            with st.expander("Sources"):
                for doc in message["sources"]:
                    source = doc.metadata.get("source", "Unknown")
                    st.markdown(f"- {source}")

# this container will be where user will ask the question
prompt = st.chat_input("Ask a question about Langchain documentation...")
if prompt:
    st.session_state["messages"].append({"role":"user", "content": prompt, "context": []})
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        st.markdown("Let me find the answer for you...")
        try:
            with st.spinner("Searching for the answer..."):
                result: Dict[str, Any] = run_llm(prompt)
                answer = str(result.get("answer","")).strip() or "Sorry, I couldn't find an answer to your question."
                sources = format_sources(result.get("context", []))
            st.markdown(answer)
            if sources:
                with st.expander("Sources"):
                    for doc in sources:
                        st.markdown(f"- {doc}")
            st.session_state.messages.append(
                {"role":"Assistant", "content": answer, "sources": sources}

            ) # Clear the "Let me find the answer for you..." message
            
        except Exception as e:
            st.error(f"An error occurred while searching for the answer: {str(e)}")
            st.stop()