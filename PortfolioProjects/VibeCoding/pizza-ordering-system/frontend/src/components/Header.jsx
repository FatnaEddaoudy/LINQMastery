import React from 'react'
import { Link } from 'react-router-dom'

const Header = ({ cartItemCount, onCartToggle }) => {
  const scrollToSection = (sectionId) => {
    const element = document.getElementById(sectionId)
    if (element) {
      element.scrollIntoView({ behavior: 'smooth' })
    }
  }

  return (
    <header className="header">
      <div className="container">
        <div className="header-content">
          <div className="logo">
            <h1><i className="fas fa-pizza-slice"></i> Tony's Pizza</h1>
          </div>
          <nav className="nav">
            <ul>
              <li><a href="#home" onClick={() => scrollToSection('home')}>Home</a></li>
              <li><a href="#menu" onClick={() => scrollToSection('menu')}>Menu</a></li>
              <li><a href="#about" onClick={() => scrollToSection('about')}>About</a></li>
              <li><a href="#contact" onClick={() => scrollToSection('contact')}>Contact</a></li>
              <li><Link to="/admin" style={{color: '#ff6b6b', textDecoration: 'none'}}>Admin</Link></li>
            </ul>
          </nav>
          <div className="cart-icon" onClick={onCartToggle}>
            <i className="fas fa-shopping-cart"></i>
            <span className="cart-count">{cartItemCount}</span>
          </div>
        </div>
      </div>
    </header>
  )
}

export default Header