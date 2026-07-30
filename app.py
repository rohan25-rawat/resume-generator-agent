from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
import langchain
from langchain.agents import create_agent
import langchain_community
from tavily import TavilyClient
import pytesseract as pyt
import streamlit as st
import os
import time
from PIL import Image
import pandas as pd
import numpy as np

#===========API Keys====================

GOOGLE_API_KEY="AQ.Ab8RN6KORQimhfthYOVjP7MnzhJCB28LprWThmRxVqb0SNKa1A"
GROQ_API_KEY= "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"
TAVILY_API_KEY = "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"

#===========Create Model================

model = ChatGoogleGenerativeAI(
    model = 'gemini-3.5-flash-lite',
    google_api_key = GOOGLE_API_KEY
)

response = model.invoke("Hello Buddy!")
response.content[-1]['text']

#=============Tools============

def search_latest_news_jobs(query):
  """This function helps to fetch latest news and jobs related article using tavily"""

  client  = TavilyClient(
      api_key=TAVILY_API_KEY)
  response = client.search(query)
  return response

  #==========Agent Creation============

  agent = create_agent(
    model = model,
    tools = [search_latest_news_jobs])
  agent

  #=======Main Agent============

def main_agent(agent, query):
  """This is main agent, or laeder agent
  that orchestrate main agents"""

  prompt = """You are AI assistant and below given
  is a prompt, your task is to give detailed prompt
  for this.
  You are a professional Resume generator where user
  will give their personal info, you have to create
  detailed resume for students or professional one
  it must be with dynamic UI and UX and advanced
  CSS professional designing, Make sure to give
  output in HTML format only no markdowns
  allowed"""

  response = agent.invoke({"messages" : [{"role" : "user",
                                          "content" : prompt}]})

  detailed_prompt = response['messages'][-1].content[-1]['text']

  with open('prompt.txt', 'w') as f:
    f.write(detailed_prompt)

  user_details = f"""Below Given is a user details
    generate Resume based on that, if not
    given keep: Default Resume: Python Developer
    user details: {query}"""

  final_prompt = prompt + detailed_prompt + user_details

  # CODE GENERATION
  response = agent. invoke({'messages': [{'role':'user',
  'content':final_prompt}]})
  code = response['messages' ][-1].content[-1]['text']

  return code  

  code = main_agent(agent, "python Developer")
  from IPython import display as DISPLAY
  DISPLAY.HTML(code)

  def get_jobs(agent,
  Location = "Noida, Delhi",
  Profile = "Data Analysts, AI Engineer"):
    Location = "Noida,Delhi"
  Profile = "Data Analysts, AI Engineer"

  prompt = f"""Based on user given Job profile,
  fetch latest jobs or job apply article
  using Naukri, Linkedin, Indeed, or all popular
  Job apply platforms, Show Results with
  JOB PROFILE NAME, LOCATION, SALARY, COMPANY NAME,need zero experience
  SHOW jobs only related to given
  {Location} and {Profile}. Output must be in
  Professional HTML Naukri theme cards with Dynamic Design,
  Show atleast Top 10-20 results with direct apply link"""

  response = agent. invoke({'messages' : [{'role':'user',
  'content':prompt}]})
  code = response['messages' ] [-1]. content[-1]['text']

  return code
