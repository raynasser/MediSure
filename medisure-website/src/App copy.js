import React, { useState } from 'react';
import './App.css';
import logo from '../src/logo.jpeg';

function App() {
  const [input, setInput] = useState('');
  const [messages, setMessages] = useState([]);

  const handleInputChange = (e) => {
    setInput(e.target.value);
  };

  const handleSend = async () => {
    if (input.trim()) {
      setMessages([...messages, { text: input, user: 'user' }]);

      try {
        const response = await fetch('http://localhost:5000/api/process-chatbot', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ text: input }),
        });

        if (!response.ok) {
          throw new Error(`Server error: ${response.status}`);
        }

        const data = await response.json();

        const formattedMessages = data.map((rec) => {
          const recommendedFoods = rec.recommended.length > 0 ? rec.recommended : ['None'];
          const foodsToAvoid = rec.to_avoid.length > 0 ? rec.to_avoid : ['None'];
          const drugsToAvoid = rec.dTo_avoid.length > 0 ? rec.dTo_avoid : ['None'];
          const sideEffects = rec.side_effects && rec.side_effects.length > 0 ? rec.side_effects : ['None'];

          return {
            text: (
              <div>
                <p>
                  <strong>For </strong>
                  <strong style={{ color: 'white' }}>{rec.drug}</strong>
                </p>
                <p><strong>Recommended foods for you</strong></p>
                <ul>
                  {recommendedFoods.map((food, i) => (
                    <li key={i}>{food}</li>
                  ))}
                </ul>
                <p><strong>Foods you should avoid</strong></p>
                <ul>
                  {foodsToAvoid.map((food, i) => (
                    <li key={i}>{food}</li>
                  ))}
                </ul>
                <p><strong>Drugs you should avoid</strong></p>
                <ul>
                  {drugsToAvoid.map((drug, i) => (
                    <li key={i}>{drug}</li>
                  ))}
                </ul>
                <p><strong style={{ color: 'white' }}>{rec.drug} </strong>
                  <strong>'s Side effects</strong></p>
                <ul>
                  {sideEffects.map((effect, i) => (
                    <li key={i}>{effect}</li>
                  ))}
                </ul>
              </div>
            ),
            user: 'bot',
          };
        });

        setMessages((prevMessages) => [...prevMessages, ...formattedMessages]);
      } catch (error) {
        console.error('Error fetching chatbot response:', error);
      }

      setInput('');
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} alt="MediSure Logo" className="logo" />
        <h1>Welcome to MediSure</h1>
        <p>Your guide to maximizing medicine efficiency through food and safe medicine interactions.</p>
      </header>

      <div className="chat-window">
        {messages.map((message, index) => (
          <div key={index} className={`message ${message.user}`}>
            {message.text}
          </div>
        ))}
      </div>

      <div className="input-group">
        <input
          className="chat-input"
          value={input}
          onChange={handleInputChange}
          onKeyPress={(e) => {
            if (e.key === 'Enter') {
              handleSend();
            }
          }}
          placeholder=" what meddicines are you using? "
        />
        <button className="chat-send-btn btn btn-primary" onClick={handleSend}>
          Send
        </button>
      </div>
    </div>
  );
}

export default App;
