import React from 'react'

const Footer = () => {
  const scrollToSection = (sectionId) => {
    const element = document.getElementById(sectionId)
    if (element) {
      element.scrollIntoView({ behavior: 'smooth' })
    }
  }

  return (
    <footer className="footer">
      <div className="container">
        <div className="footer-content">
          <div className="footer-section">
            <h3>Tony's Pizza</h3>
            <p>Authentic Italian pizza since 1975</p>
            <div className="social-links">
              <a href="#"><i className="fab fa-facebook"></i></a>
              <a href="#"><i className="fab fa-instagram"></i></a>
              <a href="#"><i className="fab fa-twitter"></i></a>
            </div>
          </div>
          <div className="footer-section">
            <h3>Quick Links</h3>
            <ul>
              <li><a href="#home" onClick={() => scrollToSection('home')}>Home</a></li>
              <li><a href="#menu" onClick={() => scrollToSection('menu')}>Menu</a></li>
              <li><a href="#about" onClick={() => scrollToSection('about')}>About</a></li>
              <li><a href="#contact" onClick={() => scrollToSection('contact')}>Contact</a></li>
            </ul>
          </div>
          <div className="footer-section">
            <h3>Contact Info</h3>
            <p><i className="fas fa-phone"></i> (555) 123-PIZZA</p>
            <p><i className="fas fa-envelope"></i> info@tonyspizza.com</p>
            <p><i className="fas fa-map-marker-alt"></i> 123 Pizza Street, Pizzaville</p>
          </div>
        </div>
        <div className="footer-bottom">
          <p>&copy; 2025 Tony's Pizza. All rights reserved.</p>
        </div>
      </div>
    </footer>
  )
}

export default Footer