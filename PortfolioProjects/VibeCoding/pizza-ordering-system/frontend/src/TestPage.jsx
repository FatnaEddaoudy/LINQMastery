import React from 'react'
import { Link } from 'react-router-dom'

const TestPage = () => {
  return (
    <div style={{ padding: '2rem', textAlign: 'center' }}>
      <h1>Test Page - Routing Works!</h1>
      <p>If you can see this page, React Router is working correctly.</p>
      <Link to="/" style={{ color: 'blue', textDecoration: 'underline' }}>
        Go back to Home
      </Link>
      <br />
      <Link to="/admin" style={{ color: 'red', textDecoration: 'underline', marginTop: '1rem', display: 'inline-block' }}>
        Go to Admin
      </Link>
    </div>
  )
}

export default TestPage