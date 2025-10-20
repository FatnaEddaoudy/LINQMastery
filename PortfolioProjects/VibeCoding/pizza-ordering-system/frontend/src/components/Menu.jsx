import React, { useState } from 'react'

const Menu = ({ pizzas, onAddToCart }) => {
  const [selectedCategory, setSelectedCategory] = useState('all')
  const [selectedSizes, setSelectedSizes] = useState({})

  const categories = [
    { id: 'all', name: 'All' },
    { id: 'classic', name: 'Classic' },
    { id: 'specialty', name: 'Specialty' },
    { id: 'vegetarian', name: 'Vegetarian' }
  ]

  const filteredPizzas = selectedCategory === 'all' 
    ? pizzas 
    : pizzas.filter(pizza => pizza.category === selectedCategory)

  const handleSizeSelect = (pizzaId, size) => {
    setSelectedSizes(prev => ({
      ...prev,
      [pizzaId]: size
    }))
  }

  const handleAddToCart = (pizza) => {
    const selectedSize = selectedSizes[pizza.id] || 'medium'
    onAddToCart(pizza, selectedSize)
    
    // Show notification
    showNotification('Added to cart!')
  }

  const showNotification = (message) => {
    const notification = document.createElement('div')
    notification.className = 'notification success show'
    notification.innerHTML = `<i class="fas fa-check"></i> ${message}`
    document.body.appendChild(notification)
    
    setTimeout(() => {
      notification.classList.remove('show')
      setTimeout(() => {
        if (document.body.contains(notification)) {
          document.body.removeChild(notification)
        }
      }, 300)
    }, 2000)
  }

  const PizzaItem = ({ pizza }) => {
    const selectedSize = selectedSizes[pizza.id] || 'medium'
    
    return (
      <div className="pizza-item">
        <div className="pizza-image">
          <img 
            src={pizza.image} 
            alt={pizza.name}
            style={{
              width: '100%',
              height: '100%',
              objectFit: 'cover',
              borderRadius: '0'
            }}
            onError={(e) => {
              e.target.style.display = 'none'
              e.target.parentNode.innerHTML = pizza.name
              e.target.parentNode.style.display = 'flex'
              e.target.parentNode.style.alignItems = 'center'
              e.target.parentNode.style.justifyContent = 'center'
              e.target.parentNode.style.background = 'linear-gradient(45deg, #ff6b6b, #feca57)'
              e.target.parentNode.style.color = 'white'
              e.target.parentNode.style.fontSize = '1.5rem'
              e.target.parentNode.style.fontWeight = 'bold'
            }}
          />
          {pizza.badge && <div className="pizza-badge">{pizza.badge}</div>}
        </div>
        <div className="pizza-info">
          <h3>{pizza.name}</h3>
          <p>{pizza.description}</p>
          <div className="pizza-price">
            ${pizza.prices[selectedSize].toFixed(2)}
          </div>
          <div className="pizza-sizes">
            {Object.entries(pizza.prices).map(([size, price]) => (
              <button
                key={size}
                className={`size-btn ${selectedSize === size ? 'active' : ''}`}
                onClick={() => handleSizeSelect(pizza.id, size)}
              >
                {size.charAt(0).toUpperCase() + size.slice(1)} - ${price.toFixed(2)}
              </button>
            ))}
          </div>
          <button className="add-to-cart" onClick={() => handleAddToCart(pizza)}>
            <i className="fas fa-plus"></i> Add to Cart
          </button>
        </div>
      </div>
    )
  }

  return (
    <section id="menu" className="menu">
      <div className="container">
        <h2 className="section-title">Our Menu</h2>
        <div className="menu-categories">
          {categories.map(category => (
            <button
              key={category.id}
              className={`category-btn ${selectedCategory === category.id ? 'active' : ''}`}
              onClick={() => setSelectedCategory(category.id)}
            >
              {category.name}
            </button>
          ))}
        </div>
        <div className="pizza-grid">
          {filteredPizzas.map(pizza => (
            <PizzaItem key={pizza.id} pizza={pizza} />
          ))}
        </div>
      </div>
    </section>
  )
}

export default Menu