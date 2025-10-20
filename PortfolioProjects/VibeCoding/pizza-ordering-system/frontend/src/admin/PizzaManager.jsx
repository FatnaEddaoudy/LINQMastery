import React, { useState, useEffect } from 'react'
import { adminService } from '../services/adminService'
import { pizzaService } from '../services/pizzaService'

const PizzaManager = () => {
  const [pizzas, setPizzas] = useState([])
  const [editingPizza, setEditingPizza] = useState(null)
  const [formData, setFormData] = useState({
    name: '',
    description: '',
    category: 'classic',
    image: '',
    badge: '',
    smallPrice: 0,
    mediumPrice: 0,
    largePrice: 0
  })

  useEffect(() => {
    loadPizzas()
  }, [])

  const loadPizzas = async () => {
    try {
      const data = await pizzaService.getAllPizzas()
      setPizzas(data)
    } catch (error) {
      console.error('Error loading pizzas:', error)
    }
  }

  const handleInputChange = (e) => {
    const { name, value } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: name.includes('Price') ? parseFloat(value) || 0 : value
    }))
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    try {
      const pizzaData = {
        ...formData,
        prices: {
          small: formData.smallPrice,
          medium: formData.mediumPrice,
          large: formData.largePrice
        }
      }

      if (editingPizza) {
        // Update existing pizza
        await fetch(`/api/pizzas/${editingPizza.id}`, {
          method: 'PUT',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            name: formData.name,
            description: formData.description,
            category: formData.category,
            image: formData.image,
            badge: formData.badge,
            smallPrice: formData.smallPrice,
            mediumPrice: formData.mediumPrice,
            largePrice: formData.largePrice
          })
        })
      } else {
        // Create new pizza
        await fetch('/api/pizzas', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            name: formData.name,
            description: formData.description,
            category: formData.category,
            image: formData.image,
            badge: formData.badge,
            smallPrice: formData.smallPrice,
            mediumPrice: formData.mediumPrice,
            largePrice: formData.largePrice
          })
        })
      }

      resetForm()
      loadPizzas()
      alert(editingPizza ? 'Pizza updated successfully!' : 'Pizza created successfully!')
    } catch (error) {
      console.error('Error saving pizza:', error)
      alert('Error saving pizza. Using local data for demo.')
    }
  }

  const handleEdit = (pizza) => {
    setEditingPizza(pizza)
    setFormData({
      name: pizza.name,
      description: pizza.description,
      category: pizza.category,
      image: pizza.image,
      badge: pizza.badge || '',
      smallPrice: pizza.prices.small,
      mediumPrice: pizza.prices.medium,
      largePrice: pizza.prices.large
    })
  }

  const handleDelete = async (pizzaId) => {
    if (!confirm('Are you sure you want to delete this pizza?')) return
    
    try {
      await fetch(`/api/pizzas/${pizzaId}`, { method: 'DELETE' })
      loadPizzas()
      alert('Pizza deleted successfully!')
    } catch (error) {
      console.error('Error deleting pizza:', error)
      alert('Error deleting pizza. This is a demo with local data.')
    }
  }

  const resetForm = () => {
    setEditingPizza(null)
    setFormData({
      name: '',
      description: '',
      category: 'classic',
      image: '',
      badge: '',
      smallPrice: 0,
      mediumPrice: 0,
      largePrice: 0
    })
  }

  return (
    <div className="pizza-manager">
      <div className="manager-header">
        <h2><i className="fas fa-pizza-slice"></i> Pizza Management</h2>
        <button className="btn-primary" onClick={resetForm}>
          <i className="fas fa-plus"></i> Add New Pizza
        </button>
      </div>

      <div className="manager-content">
        <div className="pizza-form">
          <h3>{editingPizza ? 'Edit Pizza' : 'Add New Pizza'}</h3>
          <form onSubmit={handleSubmit}>
            <div className="form-row">
              <div className="form-group">
                <label>Name:</label>
                <input
                  type="text"
                  name="name"
                  value={formData.name}
                  onChange={handleInputChange}
                  required
                />
              </div>
              <div className="form-group">
                <label>Category:</label>
                <select
                  name="category"
                  value={formData.category}
                  onChange={handleInputChange}
                >
                  <option value="classic">Classic</option>
                  <option value="specialty">Specialty</option>
                  <option value="vegetarian">Vegetarian</option>
                </select>
              </div>
            </div>

            <div className="form-group">
              <label>Description:</label>
              <textarea
                name="description"
                value={formData.description}
                onChange={handleInputChange}
                rows="3"
                required
              />
            </div>

            <div className="form-row">
              <div className="form-group">
                <label>Image URL:</label>
                <input
                  type="url"
                  name="image"
                  value={formData.image}
                  onChange={handleInputChange}
                  placeholder="https://example.com/pizza.jpg"
                />
              </div>
              <div className="form-group">
                <label>Badge (optional):</label>
                <input
                  type="text"
                  name="badge"
                  value={formData.badge}
                  onChange={handleInputChange}
                  placeholder="Popular, New, etc."
                />
              </div>
            </div>

            <div className="form-row">
              <div className="form-group">
                <label>Small Price ($):</label>
                <input
                  type="number"
                  step="0.01"
                  name="smallPrice"
                  value={formData.smallPrice}
                  onChange={handleInputChange}
                  required
                />
              </div>
              <div className="form-group">
                <label>Medium Price ($):</label>
                <input
                  type="number"
                  step="0.01"
                  name="mediumPrice"
                  value={formData.mediumPrice}
                  onChange={handleInputChange}
                  required
                />
              </div>
              <div className="form-group">
                <label>Large Price ($):</label>
                <input
                  type="number"
                  step="0.01"
                  name="largePrice"
                  value={formData.largePrice}
                  onChange={handleInputChange}
                  required
                />
              </div>
            </div>

            <div className="form-actions">
              <button type="submit" className="btn-primary">
                <i className="fas fa-save"></i> {editingPizza ? 'Update' : 'Create'} Pizza
              </button>
              {editingPizza && (
                <button type="button" className="btn-secondary" onClick={resetForm}>
                  <i className="fas fa-times"></i> Cancel
                </button>
              )}
            </div>
          </form>
        </div>

        <div className="pizza-list">
          <h3>Current Pizzas</h3>
          <div className="pizza-grid">
            {pizzas.map(pizza => (
              <div key={pizza.id} className="pizza-card">
                <div className="pizza-image">
                  <img src={pizza.image} alt={pizza.name} />
                  {pizza.badge && <span className="badge">{pizza.badge}</span>}
                </div>
                <div className="pizza-details">
                  <h4>{pizza.name}</h4>
                  <p className="category">{pizza.category}</p>
                  <p className="description">{pizza.description}</p>
                  <div className="prices">
                    <span>S: ${pizza.prices.small}</span>
                    <span>M: ${pizza.prices.medium}</span>
                    <span>L: ${pizza.prices.large}</span>
                  </div>
                  <div className="actions">
                    <button className="btn-edit" onClick={() => handleEdit(pizza)}>
                      <i className="fas fa-edit"></i> Edit
                    </button>
                    <button className="btn-delete" onClick={() => handleDelete(pizza.id)}>
                      <i className="fas fa-trash"></i> Delete
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}

export default PizzaManager