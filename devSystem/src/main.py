import asyncio
import json
import time
from web_scraper import scrape_links_to_documents
from document_processor import resize_documents #create_vectorstore
# from openai_interaction import run_chain_on
from google_serper import get_relevant_links
# from langchain_openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
import logging
from config.config import CHUNK_SIZE, CHUNK_OVERLAP


async def main():
       givenTopic = input("Enter a topic: ")
       print(f"Researching on: {givenTopic}")

       links = set(get_relevant_links(givenTopic))
       print(f"Relevant links found on Google: {len(links)}")
       print(links)

       raw_documents = await scrape_links_to_documents(list(links))
       print(f"Documents: {len(raw_documents)}")
       # print(raw_documents)

       documents = resize_documents(raw_documents, CHUNK_SIZE, CHUNK_OVERLAP)
       print(f"Split documents: {len(documents)}")
       # print(documents)

asyncio.run(main())