# Imports
from flask import Flask, request, jsonify
from langchain.tools import tool
from langchain.agents import create_agent
from rag import init_db, query_db, get_llm
from tools import create_ticket, print_ticket
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Initialize database
init_db()

# Get model and tools
model = get_llm()

template = """
The user asks: {question}

You have the following documents and their distance scores. Low scores mean the documents are
close to the user request:

{context}

Respond to the user according to the system prompt. If the distance scores are all very
high, answer as if you are unsure.
"""

# System prompt
system_prompt = """
You are SupportGenie, an AI support assistant.
- Retrieve answers from the knowledge base and cite document IDs.
- At the end of your response, include "References: [insert the document IDs you used here]"
- Be concise, professional, and avoid hallucinations.
- If unsure, say: "That information isn't available in the knowledge base."
- If the user says "open ticket" or "report issue", create a ticket by coming up with a title, a severity, and a consice summary.
- If you choose to create a ticket, include a message of the form 
"[TOOL CALL: <add your title here>ARG<add your severity here>ARG<add your summary here>]END\n\n" 
to the top of the response.
"""

agent = create_agent(model, system_prompt=system_prompt)

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
    context += str(rank) + ". id: " + res[0]["id"]
    context += "\n" + "title: " + res[0]["title"] + "\n"
    context += "content: " + res[0]["content"] + "\n"
    context += "Similarity Score: " + str(res[1]) + "\n\n"
    rank += 1

  prompt = template.format(context=context, question=query)
  answer = agent.invoke({
    "messages": [
      {"role": "user", "content": prompt}
    ]
  })

  # Locate result and check for tool calls
  answer = answer['messages'][1].content
  callidx = answer.find("]END")
  if callidx != -1:
    splits = answer.split("]END")

    # Get the actual response
    answer = splits[1].strip()

    # Parse the tool call and carry it out
    call = splits[0].replace("[TOOL CALL:","")
    args = call.split("ARG")
    ticket = create_ticket(*args)

    # Add ticket details to response
    response = "I have opened a support ticket for you:"
    response += f"\n{print_ticket(ticket)}"
    response += "\n\n" + answer
  else: 
    response = answer

  return response

# Run app and load data into the db
if __name__ == "__main__":
  app.run(debug=True)
