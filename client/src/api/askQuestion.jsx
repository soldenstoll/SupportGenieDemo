// Fetch from server
async function askQuestion(question) {
  const res = await fetch("http://127.0.0.1:5000/ask", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ query: question })
  });
  const data = await res.json();
  return data.answer;
}

export default askQuestion;
