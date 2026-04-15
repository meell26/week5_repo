import streamlit as st
from main import search

st.title("AI Travel Recommendation System")

user_input = st.text_input("Where do you want to travel?")

if user_input:
    results = search(user_input)

    st.write("Top recommendations:")
    for r in results:
        st.write(r.name)