from typing import List, Any, Dict

import streamlit as st
from backend.core import run_llm




def format_sources(context_docs:List[Any])-> List[str]:
    """Format the retrieved documents for display in the Streamlit app."""
    return [
        str(
            (meta.get("source", "Unknown")) 
            for doc in (context_docs or [])
            if (meta := getattr(doc, "metadata", None) or {})) is not None
    ]

st.set_page_config(page_title="Langchain documentation helper", layered="centered")
st.title("Langchain Documentation Helper")

with st.sidebar:
    st.subheader("Session")
    if (st.button("Clear Session", use_container_width=True)):
        st.session_state.pop("messages", None)
        st.rerun()
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role":"Assistant",
         "content":"Hello! I'm here to help you with any questions you have about Langchain. "
         "Ask me anything about the documentation, and I'll do my best to assist you!",
         "context": []
         }
    ]
for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if message.get("context"):
            with st.expander("Sources"):
                for doc in message["context"]:
                    source = doc.metadata.get("source", "Unknown")
                    st.markdown(f"- {source}")
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
                answer = str(result.get("answer")).strip() or "Sorry, I couldn't find an answer to your question."
                context_docs = format_sources(result.get("context", []))
            st.markdown(answer)
            if context_docs:
                with st.expander("Sources"):
                    for doc in context_docs:
                        st.markdown(f"- {doc}")
            st.session_state.messages.append(
                {"role":"Assistant", "content": answer, "context": context_docs}

            ) # Clear the "Let me find the answer for you..." message
            
        except Exception as e:
            st.error(f"An error occurred while searching for the answer: {str(e)}")
            st.stop()
    st.session_state["messages"] = st.session_state["messages"][-10:]
    st.rerun()
    result = run_llm(prompt)
    st.session_state["messages"].append({"role":"Assistant", "content": result["answer"], "context": result["context"]})