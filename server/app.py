# Imports
from flask import Flask, request, jsonify
from langchain.tools import tool
from langchain.agents import create_agent
from rag import init_db, query_db, get_llm
from tools import create_ticket

app = Flask(__name__)

# Get model and tools
model = get_llm()

@tool("create_ticket")
def create_ticket_tool(title, severity, summary):
  '''
  Wraps create_ticket into a tool
  '''
  return create_ticket(title, severity, summary)

tools = [create_ticket_tool]

template = """
  You have the following documents and their similarity scores:

  {context}

  The user question is: {question}

  Answer according to the system prompt. If the similarity scores are all very
  low, answer as if you are unsure.
"""

agent = create_agent(model, tools=tools)

@app.route("/ask", methods=["POST"])
def ask():
  data = request.get_json()
  query = data.get("query")
  answer = process_query(query)
  return jsonify({"answer": answer})

def process_query(query):
  '''
  Function for processing a query. Outputs the model's response as
  a string.
  '''
  # Query db for faqs
  results = query_db(query)

  # Format results into template
  context = ""
  rank = 1
  for res in results:
    context += str(rank) + ". Content: " + str(res[0])
    context += ", Similarity Score: " + str(res[1]) + "\n\n"

  prompt = template.format(context=context, question=query)
  answer = agent.invoke({"input": prompt})

  # Output result
  return answer

# Run app and load data into the db
if __name__ == "__main__":
  init_db()
  app.run()
