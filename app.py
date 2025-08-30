# import streamlit as st
# import requests

# st.set_page_config(page_title="HR Resource Query Chatbot", page_icon="", layout="centered")

# st.title(" HR Resource Query Chatbot")
# st.caption("Ask in natural language. Example: *Find Python developers with 3+ years experience in Bengaluru.*")

# backend_url = st.text_input("Backend URL", value="http://localhost:8000", help="FastAPI server base URL")

# query = st.text_input("Your query")
# if st.button("Search") and query.strip():
#     try:
#         resp = requests.post(f"{backend_url}/chat", json={"query": query}, timeout=60)
#         resp.raise_for_status()
#         data = resp.json()
#         st.subheader("Response")
#         st.write(data.get("response", ""))

#         st.subheader("Matched Employees")
#         emps = data.get("employees", [])
#         for e in emps:
#             st.markdown(f"- **{e['name']}**, {e['role']} — {', '.join(e['skills'])} "
#                         f"· {e['experience_years']} yrs · {e['location']} · {e['email']}")
#     except Exception as e:
#         st.error(f"Failed to contact backend: {e}")

# st.divider()
# st.markdown("**Tip:** Set the `GEMINI_API_KEY` environment variable before starting the backend to enable LLM responses.")
import streamlit as st
import requests

# Use robo.png as page icon (must be in same folder as app.py)
# st.set_page_config(
#     page_title="HR Resource Query Chatbot",
#     page_icon="robo.png",   # ✅ this will show your PNG as favicon
#     layout="centered"
# )

# st.title("🤖 HR Resource Query Chatbot")
# st.caption("Ask in natural language. Example: *Find Python developers with 3+ years experience in Bengaluru.*")

# backend_url = st.text_input("Backend URL", value="http://localhost:8000", help="FastAPI server base URL")

# query = st.text_input("Your query")
# if st.button("Search") and query.strip():
#     try:
#         resp = requests.post(f"{backend_url}/chat", json={"query": query}, timeout=60)
#         resp.raise_for_status()
#         data = resp.json()
#         st.subheader("Response")
#         st.write(data.get("response", ""))

#         st.subheader("Matched Employees")
#         emps = data.get("employees", [])
#         for e in emps:
#             st.markdown(f"- **{e['name']}**, {e['role']} — {', '.join(e['skills'])} "
#                         f"· {e['experience_years']} yrs · {e['location']} · {e['email']}")
#     except Exception as e:
#         st.error(f"Failed to contact backend: {e}")

# st.divider()
# st.markdown("**Tip:** Set the `GEMINI_API_KEY` environment variable before starting the backend to enable LLM responses.")
import streamlit as st
import requests

# ✅ Use robo.png as favicon
st.set_page_config(
    page_title="HR Resource Query Chatbot",
    page_icon="robo.png",
    layout="centered"
)

# ✅ Display logo + title together
col1, col2 = st.columns([1, 8])  # adjust ratio if needed
with col1:
    st.image("robo.png", width=60)  # show your icon inside app
with col2:
    st.title("Sourav's HR Resource Chatbot")

st.caption("Ask in natural language. Example: *Find Python developers with 3+ years experience in Bengaluru.*")

backend_url = st.text_input("Backend URL", value="http://localhost:8000", help="FastAPI server base URL")

query = st.text_input("Your query")
if st.button("Search") and query.strip():
    try:
        resp = requests.post(f"{backend_url}/chat", json={"query": query}, timeout=60)
        resp.raise_for_status()
        data = resp.json()
        st.subheader("Response")
        st.write(data.get("response", ""))

        st.subheader("Matched Employees")
        emps = data.get("employees", [])
        for e in emps:
            st.markdown(f"- **{e['name']}**, {e['role']} — {', '.join(e['skills'])} "
                        f"· {e['experience_years']} yrs · {e['location']} · {e['email']}")
    except Exception as e:
        st.error(f"Failed to contact backend: {e}")

st.divider()
st.markdown("**Tip:** Set the `GEMINI_API_KEY` environment variable before starting the backend to enable LLM responses.")
