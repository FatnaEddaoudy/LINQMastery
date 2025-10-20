// Pizza service for API calls and local data
const API_BASE_URL = '/api'

const pizzaData = [
  {
    id: 1,
    name: "Margherita",
    description: "Fresh tomatoes, mozzarella cheese, basil, and olive oil",
    category: "classic",
    image: "https://images.unsplash.com/photo-1574071318508-1cdbab80d002?w=400&h=300&fit=crop&crop=center",
    prices: { small: 12.99, medium: 16.99, large: 20.99 },
    badge: "Popular"
  },
  {
    id: 2,
    name: "Pepperoni",
    description: "Classic pepperoni with mozzarella cheese and tomato sauce",
    category: "classic",
    image: "https://images.unsplash.com/photo-1628840042765-356cda07504e?w=400&h=300&fit=crop&crop=center",
    prices: { small: 14.99, medium: 18.99, large: 22.99 },
    badge: "Best Seller"
  },
  {
    id: 3,
    name: "Supreme",
    description: "Pepperoni, sausage, mushrooms, bell peppers, onions, and olives",
    category: "specialty",
    image: "https://images.unsplash.com/photo-1571997478779-2adcbbe9ab2f?w=400&h=300&fit=crop&crop=center",
    prices: { small: 18.99, medium: 22.99, large: 26.99 },
    badge: "Chef's Choice"
  },
  {
    id: 4,
    name: "Hawaiian",
    description: "Ham, pineapple, and mozzarella cheese",
    category: "specialty",
    image: "https://images.unsplash.com/photo-1565299624946-b28f40a0ca4b?w=400&h=300&fit=crop&crop=center",
    prices: { small: 16.99, medium: 20.99, large: 24.99 },
    badge: ""
  },
  {
    id: 5,
    name: "Vegetarian Deluxe",
    description: "Mushrooms, bell peppers, onions, tomatoes, and olives",
    category: "vegetarian",
    image: "https://images.unsplash.com/photo-1593560708920-61dd61444791?w=400&h=300&fit=crop&crop=center",
    prices: { small: 15.99, medium: 19.99, large: 23.99 },
    badge: "Healthy"
  },
  {
    id: 6,
    name: "Meat Lovers",
    description: "Pepperoni, sausage, ham, bacon, and ground beef",
    category: "specialty",
    image: "https://images.unsplash.com/photo-1594007654729-407eedc4be65?w=400&h=300&fit=crop&crop=center",
    prices: { small: 19.99, medium: 24.99, large: 28.99 },
    badge: "Protein Packed"
  },
  {
    id: 7,
    name: "BBQ Chicken",
    description: "Grilled chicken, BBQ sauce, red onions, and cilantro",
    category: "specialty",
    image: "https://images.unsplash.com/photo-1513104890138-7c749659a591?w=400&h=300&fit=crop&crop=center",
    prices: { small: 17.99, medium: 21.99, large: 25.99 },
    badge: ""
  },
  {
    id: 8,
    name: "Four Cheese",
    description: "Mozzarella, parmesan, cheddar, and goat cheese",
    category: "classic",
    image: "https://images.unsplash.com/photo-1541745537411-b8046dc6d66c?w=400&h=300&fit=crop&crop=center",
    prices: { small: 16.99, medium: 20.99, large: 24.99 },
    badge: "Cheese Lovers"
  },
  {
    id: 9,
    name: "Mediterranean",
    description: "Feta cheese, olives, tomatoes, red onions, and herbs",
    category: "vegetarian",
    image: "https://images.unsplash.com/photo-1579952363873-27d3bfad9c0d?w=400&h=300&fit=crop&crop=center",
    prices: { small: 17.99, medium: 21.99, large: 25.99 },
    badge: "Fresh"
  },
  {
    id: 10,
    name: "Buffalo Chicken",
    description: "Buffalo chicken, celery, red onions, and ranch dressing",
    category: "specialty",
    image: "https://images.unsplash.com/photo-1555072956-7758afb20e8f?w=400&h=300&fit=crop&crop=center",
    prices: { small: 18.99, medium: 22.99, large: 26.99 },
    badge: "Spicy"
  },
  {
    id: 11,
    name: "Veggie Supreme",
    description: "Spinach, artichokes, sun-dried tomatoes, and feta cheese",
    category: "vegetarian",
    image: "https://images.unsplash.com/photo-1552539618-7eec9b4d1796?w=400&h=300&fit=crop&crop=center",
    prices: { small: 16.99, medium: 20.99, large: 24.99 },
    badge: "Gourmet"
  },
  {
    id: 12,
    name: "White Pizza",
    description: "Ricotta, mozzarella, garlic, and fresh herbs",
    category: "classic",
    image: "https://images.unsplash.com/photo-1585238342024-78d387f4a707?w=400&h=300&fit=crop&crop=center",
    prices: { small: 15.99, medium: 19.99, large: 23.99 },
    badge: ""
  }
]

export const pizzaService = {
  // Get all pizzas from API or return local data
  async getAllPizzas() {
    try {
      const response = await fetch(`${API_BASE_URL}/pizzas`)
      if (!response.ok) {
        throw new Error('Failed to fetch pizzas')
      }
      return await response.json()
    } catch (error) {
      console.log('API not available, using local data')
      return this.getLocalPizzas()
    }
  },

  // Get local pizza data
  getLocalPizzas() {
    return pizzaData
  },

  // Get pizza by ID
  async getPizzaById(id) {
    try {
      const response = await fetch(`${API_BASE_URL}/pizzas/${id}`)
      if (!response.ok) {
        throw new Error('Failed to fetch pizza')
      }
      return await response.json()
    } catch (error) {
      return pizzaData.find(pizza => pizza.id === id)
    }
  },

  // Submit order
  async submitOrder(orderData) {
    try {
      const response = await fetch(`${API_BASE_URL}/orders`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(orderData),
      })
      
      if (!response.ok) {
        throw new Error('Failed to submit order')
      }
      
      return await response.json()
    } catch (error) {
      console.error('Order submission failed:', error)
      // Return mock success for demo
      return {
        id: Date.now(),
        status: 'confirmed',
        estimatedDelivery: new Date(Date.now() + 30 * 60 * 1000) // 30 minutes
      }
    }
  },

  // Submit contact form
  async submitContactForm(formData) {
    try {
      const response = await fetch(`${API_BASE_URL}/contact`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      })
      
      if (!response.ok) {
        throw new Error('Failed to submit contact form')
      }
      
      return await response.json()
    } catch (error) {
      console.error('Contact form submission failed:', error)
      // Return mock success for demo
      return { success: true, message: 'Message received' }
    }
  }
}