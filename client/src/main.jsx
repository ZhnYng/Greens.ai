import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.jsx'
import './index.css'
import axios from 'axios'

// axios.defaults.baseURL = "http://127.0.0.1:5000"
axios.defaults.baseURL = "https://greens-ai.onrender.com"
ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)
