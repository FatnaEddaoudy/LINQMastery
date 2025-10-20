import React, { useState } from 'react'
import { pizzaService } from '../services/pizzaService'

const Cart = ({ 
  isOpen, 
  items, 
  totalPrice, 
  onClose, 
  onUpdateQuantity, 
  onRemoveItem, 
  onClearCart 
}) => {
  const [showCheckout, setShowCheckout] = useState(false)
  const [customerInfo, setCustomerInfo] = useState({
    name: '',
    email: '',
    phone: '',
    address: '',
    city: '',
    zipCode: '',
    specialInstructions: ''
  })
  const [isSubmitting, setIsSubmitting] = useState(false)

  const handleInputChange = (e) => {
    const { name, value } = e.target
    setCustomerInfo(prev => ({
      ...prev,
      [name]: value
    }))
  }

  const handleCheckout = () => {
    if (items.length === 0) {
      alert('Your cart is empty!')
      return
    }
    setShowCheckout(true)
  }

  const handleBackToCart = () => {
    setShowCheckout(false)
  }

  const handleSubmitOrder = async (e) => {
    e.preventDefault()
    setIsSubmitting(true)

    try {
      const orderData = {
        customerName: customerInfo.name,
        customerEmail: customerInfo.email,
        customerPhone: customerInfo.phone,
        deliveryAddress: `${customerInfo.address}, ${customerInfo.city}, ${customerInfo.zipCode}`,
        specialInstructions: customerInfo.specialInstructions,
        items: items.map(item => ({
          pizzaId: item.pizzaId,
          pizzaName: item.name,
          size: item.size,
          quantity: item.quantity,
          unitPrice: item.price,
          totalPrice: item.price * item.quantity
        })),
        totalAmount: totalPrice,
        orderDate: new Date().toISOString()
      }

      const result = await pizzaService.submitOrder(orderData)
      
      alert(`Order submitted successfully! Order #${result.id}\n\nEstimated delivery: 25-35 minutes\nTotal: $${totalPrice.toFixed(2)}\n\nThank you for choosing Tony's Pizza!`)
      
      // Reset form and cart
      setCustomerInfo({
        name: '',
        email: '',
        phone: '',
        address: '',
        city: '',
        zipCode: '',
        specialInstructions: ''
      })
      setShowCheckout(false)
      onClearCart()
      onClose()
    } catch (error) {
      console.error('Order submission failed:', error)
      alert('Failed to submit order. Please try again.')
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <>
      <div className={`cart-overlay ${isOpen ? 'active' : ''}`} onClick={onClose}></div>
      <div className={`cart-sidebar ${isOpen ? 'open' : ''}`}>
        {!showCheckout ? (
          // Cart View
          <>
            <div className="cart-header">
              <h3>Shopping Cart</h3>
              <button className="close-cart" onClick={onClose}>
                <i className="fas fa-times"></i>
              </button>
            </div>
            
            <div className="cart-items">
              {items.length === 0 ? (
                <div style={{ textAlign: 'center', padding: '2rem', color: '#666' }}>
                  Your cart is empty
                </div>
              ) : (
                items.map(item => (
                  <div key={item.id} className="cart-item">
                    <div className="cart-item-image">
                      <img src={item.image} alt={item.name} style={{width: '50px', height: '50px', objectFit: 'cover', borderRadius: '8px'}} />
                    </div>
                    <div className="cart-item-info">
                      <h4>{item.name}</h4>
                      <p>Size: {item.size.charAt(0).toUpperCase() + item.size.slice(1)}</p>
                    </div>
                    <div className="cart-item-controls">
                      <button 
                        className="quantity-btn" 
                        onClick={() => onUpdateQuantity(item.id, -1)}
                      >
                        -
                      </button>
                      <span className="quantity">{item.quantity}</span>
                      <button 
                        className="quantity-btn" 
                        onClick={() => onUpdateQuantity(item.id, 1)}
                      >
                        +
                      </button>
                      <button 
                        className="remove-item" 
                        onClick={() => onRemoveItem(item.id)}
                      >
                        <i className="fas fa-trash"></i>
                      </button>
                    </div>
                    <div className="cart-item-price">
                      ${(item.price * item.quantity).toFixed(2)}
                    </div>
                  </div>
                ))
              )}
            </div>
            
            <div className="cart-footer">
              <div className="cart-total">
                <strong>Total: ${totalPrice.toFixed(2)}</strong>
              </div>
              <button className="checkout-btn" onClick={handleCheckout} disabled={items.length === 0}>
                Proceed to Checkout
              </button>
            </div>
          </>
        ) : (
          // Checkout View
          <>
            <div className="cart-header">
              <h3>Checkout</h3>
              <button className="close-cart" onClick={onClose}>
                <i className="fas fa-times"></i>
              </button>
            </div>
            
            <div className="checkout-content">
              <button className="back-btn" onClick={handleBackToCart} style={{marginBottom: '1rem', background: '#6c757d', color: 'white', border: 'none', padding: '0.5rem 1rem', borderRadius: '4px'}}>
                <i className="fas fa-arrow-left"></i> Back to Cart
              </button>
              
              <form onSubmit={handleSubmitOrder}>
                <div className="form-section">
                  <h4>Contact Information</h4>
                  <div className="form-group">
                    <input
                      type="text"
                      name="name"
                      placeholder="Full Name *"
                      value={customerInfo.name}
                      onChange={handleInputChange}
                      required
                    />
                  </div>
                  <div className="form-group">
                    <input
                      type="email"
                      name="email"
                      placeholder="Email Address *"
                      value={customerInfo.email}
                      onChange={handleInputChange}
                      required
                    />
                  </div>
                  <div className="form-group">
                    <input
                      type="tel"
                      name="phone"
                      placeholder="Phone Number *"
                      value={customerInfo.phone}
                      onChange={handleInputChange}
                      required
                    />
                  </div>
                </div>

                <div className="form-section">
                  <h4>Delivery Address</h4>
                  <div className="form-group">
                    <input
                      type="text"
                      name="address"
                      placeholder="Street Address *"
                      value={customerInfo.address}
                      onChange={handleInputChange}
                      required
                    />
                  </div>
                  <div className="form-row">
                    <div className="form-group">
                      <input
                        type="text"
                        name="city"
                        placeholder="City *"
                        value={customerInfo.city}
                        onChange={handleInputChange}
                        required
                      />
                    </div>
                    <div className="form-group">
                      <input
                        type="text"
                        name="zipCode"
                        placeholder="ZIP Code *"
                        value={customerInfo.zipCode}
                        onChange={handleInputChange}
                        required
                      />
                    </div>
                  </div>
                  <div className="form-group">
                    <textarea
                      name="specialInstructions"
                      placeholder="Special delivery instructions (optional)"
                      value={customerInfo.specialInstructions}
                      onChange={handleInputChange}
                      rows="3"
                    />
                  </div>
                </div>

                <div className="order-summary">
                  <h4>Order Summary</h4>
                  {items.map(item => (
                    <div key={item.id} className="summary-item">
                      <span>{item.name} ({item.size}) x{item.quantity}</span>
                      <span>${(item.price * item.quantity).toFixed(2)}</span>
                    </div>
                  ))}
                  <div className="summary-total">
                    <strong>Total: ${totalPrice.toFixed(2)}</strong>
                  </div>
                </div>

                <button 
                  type="submit" 
                  className="place-order-btn"
                  disabled={isSubmitting}
                >
                  {isSubmitting ? 'Placing Order...' : `Place Order - $${totalPrice.toFixed(2)}`}
                </button>
              </form>
            </div>
          </>
        )}
      </div>
    </>
  )
}

export default Cart