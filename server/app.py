# Imports
from flask import Flask, request, jsonify
from rag import get_retriever, add_documents, get_llm
from langchain.chains import RetrievalQA
import json

# Data location
DOCS_PATH = "./data/kb_seed/support_kb.json"

app = Flask(__name__)


def init_db():
  try:
    with open(DOCS_PATH, 'r') as f:
      data = json.load(f)
    

  except FileNotFoundError:
    print(f"Error: The file '{DOCS_PATH}' was not found.")
  except json.JSONDecodeError:
      print(f"Error: Could not decode JSON from '{DOCS_PATH}'. Check if the file contains valid JSON.")
  except Exception as e:
      print(f"An unexpected error occurred: {e}")

# Run app and load data into the db
if __name__ == "__main__":
  init_db()
  app.run()
