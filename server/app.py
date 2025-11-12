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
- The user asks: {question}
- You have the following documents and their distance scores. Low scores mean the documents are
close to the user request. Use these if they are helpful for answering the user's question:

{context}

- If you use content from a document in your response, at the end of your response, include a message stating
"References: [insert the document IDs you used here]"
- To create a ticket, come up with a title, severtiy, and summary, and include a message in the format:
"[TOOL CALL: <add your title here>ARG<add your severity here>ARG<add your summary here>]END\n\n" 
at the very start of your response.
- If all of the documents have high distance scores and are not useful to your answer, respond as if you are
unsure.

EXAMPLES:
- If the user asks: "How do I reset my password?", 
You should respond with something like:
To reset your password, go to Settings > Security.  If Two-Factor Authentication (2FA) is enabled, 
you'll need a backup code or registered device. 

References: [faq_01].

- If the user says: "Open a support ticket so they can talk to someone"
Respond with something like:
[TOOL CALL: Connecting with a support memberARGMediumARGUser wants to speak to a representative]END

Let me know if you have any other questions!
"""

# System prompt
system_prompt = """
You are SupportGenie, an AI support assistant.
- Retrieve answers from the knowledge base and cite document IDs.
- If the user says "open ticket" or "report issue", call the tool `create_ticket` with title, severity, and summary.
- Be concise, professional, and avoid hallucinations.
- If unsure, say: "That information isn't available in the knowledge base."
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
