# Imports
from flask import Flask, request, jsonify
from rag import init_db, get_retriever, add_documents, get_llm

app = Flask(__name__)




# Run app and load data into the db
if __name__ == "__main__":
  init_db()
  app.run()
