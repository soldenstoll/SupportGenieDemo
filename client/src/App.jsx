import React, { useState, useRef, useEffect } from 'react'
import './App.css'
import askQuestion from './api/askQuestion'

function App() {
  const [messages, setMessages] = useState([
    { id: 1, from: 'bot', text: 'Hi — how can I help you today?' },
  ])
  const [input, setInput] = useState('')
  const messagesEndRef = useRef(null)

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  function sendMessage() {
    const text = input.trim()
    if (!text) return
    const userMsg = { id: Date.now(), from: 'user', text }
    setMessages((m) => [...m, userMsg])
    setInput('')

    // Query server for model response
    const response = askQuestion(text)
    setMessages((m) => [
      ...m,
      { id: Date.now() + 1, from: 'bot', text: response },
    ])
  }

  function handleKeyDown(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      sendMessage()
    }
  }

  return (
    <div className="page">
      <div className="chat-container" role="main">
        <header className="main-header">
          <div className="brand-inline">SupportGenie</div>
          <h2>How can I help you?</h2>
          <p className="subtitle">Ask a question or paste logs — I'll try to help.</p>
        </header>

        <section className="chat">
          <div className="messages" aria-live="polite">
            {messages.map((m) => (
              <div key={m.id} className={`message ${m.from}`}>
                <div className="bubble">{m.text}</div>
              </div>
            ))}
            <div ref={messagesEndRef} />
          </div>

          <form
            className="composer"
            onSubmit={(e) => {
              e.preventDefault()
              sendMessage()
            }}
          >
            <div className="composer-inner">
              <textarea
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={handleKeyDown}
                placeholder="Ask a question or describe your issue..."
                aria-label="Message"
              />
              <button type="submit" className="send" aria-label="Send message">Send</button>
            </div>
          </form>
        </section>
      </div>
    </div>
  )
}

export default App
