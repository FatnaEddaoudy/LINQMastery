import axios from 'axios'

const API_BASE_URL = 'http://localhost:5000/api'

export const adminService = {
  // Orders API
  async getAllOrders() {
    try {
      const response = await axios.get(`${API_BASE_URL}/orders`)
      return response.data
    } catch (error) {
      console.error('Failed to fetch orders:', error)
      return []
    }
  },

  async getOrderById(id) {
    try {
      const response = await axios.get(`${API_BASE_URL}/orders/${id}`)
      return response.data
    } catch (error) {
      console.error('Failed to fetch order:', error)
      return null
    }
  },

  async updateOrderStatus(id, status) {
    try {
      const response = await axios.patch(`${API_BASE_URL}/orders/${id}/status`, JSON.stringify(status), {
        headers: {
          'Content-Type': 'application/json'
        }
      })
      return response.data
    } catch (error) {
      console.error('Failed to update order status:', error)
      throw error
    }
  },

  // Messages API
  async getAllMessages() {
    try {
      const response = await axios.get(`${API_BASE_URL}/contact`)
      return response.data
    } catch (error) {
      console.error('Failed to fetch messages:', error)
      return []
    }
  },

  async markMessageAsRead(id) {
    try {
      const response = await axios.patch(`${API_BASE_URL}/contact/${id}/read`)
      return response.data
    } catch (error) {
      console.error('Failed to mark message as read:', error)
      throw error
    }
  },

  async replyToMessage(id, reply) {
    try {
      const response = await axios.post(`${API_BASE_URL}/contact/${id}/reply`, {
        reply: reply
      })
      return response.data
    } catch (error) {
      console.error('Failed to send reply:', error)
      throw error
    }
  },

  // Pizzas API
  async getAllPizzas() {
    try {
      const response = await axios.get(`${API_BASE_URL}/pizzas`)
      return response.data
    } catch (error) {
      console.error('Failed to fetch pizzas:', error)
      return []
    }
  },

  async createPizza(pizzaData) {
    try {
      const response = await axios.post(`${API_BASE_URL}/pizzas`, pizzaData)
      return response.data
    } catch (error) {
      console.error('Failed to create pizza:', error)
      throw error
    }
  },

  async updatePizza(id, pizzaData) {
    try {
      const response = await axios.put(`${API_BASE_URL}/pizzas/${id}`, pizzaData)
      return response.data
    } catch (error) {
      console.error('Failed to update pizza:', error)
      throw error
    }
  },

  async deletePizza(id) {
    try {
      const response = await axios.delete(`${API_BASE_URL}/pizzas/${id}`)
      return response.data
    } catch (error) {
      console.error('Failed to delete pizza:', error)
      throw error
    }
  }
}