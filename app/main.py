import streamlit as st
from langchain_community.document_loaders import WebBaseLoader

from chain import Chain
from portfolio import Portfolio
from utils import clean_text


def create_streamlit_app(chain, portfolio, clean_text):
    st.title("Cold Email Generator")

    url_input = st.text_input("Enter the URL of the job posting", value = "https://jobs.nike.com/job/R-43863?from=job%20search%20funnel")
    submit_btn = st.button("Submit")

    if submit_btn:
        try:
            loader = WebBaseLoader([url_input])
            data = clean_text(loader.load().pop().page_content)
            portfolio.load_portfolio()
            jobs = chain.extract_jobs(data)
            for job in jobs:
                skills = job.get('skills', [])
                links = portfolio.query_links(skills)
                email = chain.email_generator(job, links)
                st.code(email)
        except Exception as e:
            st.error(f"An error occurred: {e}")         

if __name__ == "__main__":
    chain = Chain()
    portfolio = Portfolio()
    st.set_page_config(layout="wide", page_title="Cold Email Generator", page_icon="📧")
    create_streamlit_app(chain, portfolio, clean_text)     