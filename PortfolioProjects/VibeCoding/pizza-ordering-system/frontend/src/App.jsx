import React, { useState, useEffect } from 'react'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Header from './components/Header'
import Hero from './components/Hero'
import Menu from './components/Menu'
import About from './components/About'
import Contact from './components/Contact'
import Cart from './components/Cart'
import Footer from './components/Footer'
import Admin from './admin/Admin'
import TestPage from './TestPage'
import { pizzaService } from './services/pizzaService'
import './App.css'

function App() {
  const [pizzas, setPizzas] = useState([])
  const [cart, setCart] = useState([])
  const [isCartOpen, setIsCartOpen] = useState(false)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadPizzas()
    loadCartFromStorage()
  }, [])

  const loadPizzas = async () => {
    try {
      const data = await pizzaService.getAllPizzas()
      setPizzas(data)
    } catch (error) {
      console.error('Error loading pizzas:', error)
      // Fallback to local data if API fails
      setPizzas(pizzaService.getLocalPizzas())
    } finally {
      setLoading(false)
    }
  }

  const loadCartFromStorage = () => {
    const savedCart = localStorage.getItem('pizzaCart')
    if (savedCart) {
      setCart(JSON.parse(savedCart))
    }
  }

  const saveCartToStorage = (newCart) => {
    localStorage.setItem('pizzaCart', JSON.stringify(newCart))
  }

  const addToCart = (pizza, size) => {
    const existingItem = cart.find(
      item => item.pizzaId === pizza.id && item.size === size
    )

    let newCart
    if (existingItem) {
      newCart = cart.map(item =>
        item.pizzaId === pizza.id && item.size === size
          ? { ...item, quantity: item.quantity + 1 }
          : item
      )
    } else {
      const newItem = {
        id: Date.now(),
        pizzaId: pizza.id,
        name: pizza.name,
        size,
        price: pizza.prices[size],
        quantity: 1,
        image: pizza.image
      }
      newCart = [...cart, newItem]
    }

    setCart(newCart)
    saveCartToStorage(newCart)
  }

  const updateCartQuantity = (itemId, change) => {
    const newCart = cart.map(item => {
      if (item.id === itemId) {
        const newQuantity = item.quantity + change
        return newQuantity > 0 ? { ...item, quantity: newQuantity } : null
      }
      return item
    }).filter(Boolean)

    setCart(newCart)
    saveCartToStorage(newCart)
  }

  const removeFromCart = (itemId) => {
    const newCart = cart.filter(item => item.id !== itemId)
    setCart(newCart)
    saveCartToStorage(newCart)
  }

  const clearCart = () => {
    setCart([])
    saveCartToStorage([])
  }

  const getTotalItems = () => {
    return cart.reduce((total, item) => total + item.quantity, 0)
  }

  const getTotalPrice = () => {
    return cart.reduce((total, item) => total + (item.price * item.quantity), 0)
  }

  if (loading) {
    return (
      <div className="loading-screen">
        <div className="loading-spinner">
          <i className="fas fa-pizza-slice"></i>
          <p>Loading delicious pizzas...</p>
        </div>
      </div>
    )
  }

  return (
    <Router>
      <div className="App">
        <Routes>
          <Route path="/test" element={<TestPage />} />
          <Route path="/admin/*" element={<Admin />} />
          <Route path="/" element={
            <>
              <Header 
                cartItemCount={getTotalItems()}
                onCartToggle={() => setIsCartOpen(!isCartOpen)}
              />
              
              <Hero />
              
              <Menu 
                pizzas={pizzas}
                onAddToCart={addToCart}
              />
              
              <About />
              
              <Contact />
              
              <Cart
                isOpen={isCartOpen}
                items={cart}
                totalPrice={getTotalPrice()}
                onClose={() => setIsCartOpen(false)}
                onUpdateQuantity={updateCartQuantity}
                onRemoveItem={removeFromCart}
                onClearCart={clearCart}
              />
              
              <Footer />
            </>
          } />
        </Routes>
      </div>
    </Router>
  )
}

export default App