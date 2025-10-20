import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import PizzaManager from './PizzaManager';
import OrderManager from './OrderManager';
import MessageManager from './MessageManager';
import './Admin.css';

const Admin = () => {
  const [activeTab, setActiveTab] = useState('pizzas')
  const [isAuthenticated, setIsAuthenticated] = useState(false)
  const [password, setPassword] = useState('')

  const adminPassword = 'admin123' // In real app, use proper authentication

  const handleLogin = (e) => {
    e.preventDefault()
    if (password === adminPassword) {
      setIsAuthenticated(true)
      // Removed localStorage persistence for security
    } else {
      alert('Invalid password!')
    }
  }

  const handleLogout = () => {
    setIsAuthenticated(false)
    setPassword('')
  }

  useEffect(() => {
    // Always start with unauthenticated state for better security
    setIsAuthenticated(false)
  }, [])

  if (!isAuthenticated) {
    return (
      <div className="admin-login">
        <div className="login-form">
          <h2><i className="fas fa-shield-alt"></i> Admin Login</h2>
          <form onSubmit={handleLogin}>
            <input
              type="password"
              placeholder="Enter admin password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
            <button type="submit">Login</button>
          </form>
          <p className="login-hint">Hint: admin123</p>
        </div>
      </div>
    )
  }

  return (
    <div className="admin-panel">
      <div className="admin-header">
        <h1><i className="fas fa-cog"></i> Admin Panel</h1>
        <div>
          <Link to="/" className="logout-btn" style={{ marginRight: '10px', textDecoration: 'none' }}>
            <i className="fas fa-home"></i> Back to Website
          </Link>
          <button className="logout-btn" onClick={handleLogout}>
            <i className="fas fa-sign-out-alt"></i> Logout
          </button>
        </div>
      </div>
      
      <div className="admin-nav">
        <button 
          className={`nav-btn ${activeTab === 'pizzas' ? 'active' : ''}`}
          onClick={() => setActiveTab('pizzas')}
        >
          <i className="fas fa-pizza-slice"></i> Manage Pizzas
        </button>
        <button 
          className={`nav-btn ${activeTab === 'orders' ? 'active' : ''}`}
          onClick={() => setActiveTab('orders')}
        >
          <i className="fas fa-shopping-cart"></i> View Orders
        </button>
        <button 
          className={`nav-btn ${activeTab === 'messages' ? 'active' : ''}`}
          onClick={() => setActiveTab('messages')}
        >
          <i className="fas fa-envelope"></i> Contact Messages
        </button>
      </div>

      <div className="admin-content">
        {activeTab === 'pizzas' && <PizzaManager />}
        {activeTab === 'orders' && <OrderManager />}
        {activeTab === 'messages' && <MessageManager />}
      </div>
    </div>
  )
}

export default Admin