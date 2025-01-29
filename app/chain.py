from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException

from dotenv import load_dotenv
import os

load_dotenv()

class Chain:
    def __init__(self):
        self.llama = ChatGroq(
            model="llama-3.3-70b-versatile",
            temperature=0,
            groq_api_key=os.getenv("GROQ_API_KEY")
        )

    def extract_jobs(self, cleaned_text):
        prompt_extract = PromptTemplate.from_template(
            """
            ###SCRAPED TEXT FROM WEBSITE:
            {page_content}
            ###INSTRUCTIONS:
            The scaped text is from the career's page of a website.
            Your job is to extract the job postings and return them in JSON format containing the following keys: `role`, `experience`, `skills` and `description`.
            Only return the valid JSON.
            ###VALID JSON(NO PREAMBLE):
            """
        )

        chain_extract = prompt_extract | self.llama
        json = chain_extract.invoke(input={'page_content':cleaned_text})

        try:
            json_parser = JsonOutputParser()
            res = json_parser.parse(json.content)
        except OutputParserException:
            raise OutputParserException("Context too big. Unable to parse jobs.")
        return res if isinstance(res, list) else [res]

    def email_generator(self, job_description, links):
        prompt_email = PromptTemplate.from_template(
            """
            ###JOB DESCRIPTION:
            {job_description}

            ###INSTRUCTION:
            You are George, a business development executive at AtliQ. AtliQ is an AI and software consultancy company dedicated to facilitate the seamless
            integration of the business processes through automated tools.
            Over our experience, we have empowered numerous enterprises with tailored solutions, fostering sclability, process optimization, cost reduction,
            heightened overall efficiency.
            Your job is to write cold email to the client regarding the job mentioned above describing the capability of atliQ in fulfilling their needs.
            Also add the most relevent one from the following list to showcase Atliq's portfolio: {link_list}
            Remember, you are BDE in atliq.
            Do not provide a preamble.

            ###EMAIL (NO PREAMBLE):
            """)
        chain_email = prompt_email | self.llama
        email_res = chain_email.invoke({"job_description": str(job_description), "link_list": links})
        return email_res.content
    

