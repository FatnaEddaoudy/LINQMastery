import React from 'react'

const Hero = () => {
  const scrollToMenu = () => {
    const menuElement = document.getElementById('menu')
    if (menuElement) {
      menuElement.scrollIntoView({ behavior: 'smooth' })
    }
  }

  return (
    <section id="home" className="hero">
      <div className="hero-content">
        <h2>Authentic Italian Pizza</h2>
        <p>Fresh ingredients, traditional recipes, delivered hot to your door</p>
        <button className="cta-button" onClick={scrollToMenu}>
          Order Now
        </button>
      </div>
    </section>
  )
}

export default Hero