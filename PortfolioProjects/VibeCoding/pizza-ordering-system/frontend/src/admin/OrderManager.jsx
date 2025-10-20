import React, { useState, useEffect } from 'react'
import { adminService } from '../services/adminService'

const OrderManager = () => {
  const [orders, setOrders] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadOrders()
  }, [])

  const loadOrders = async () => {
    setLoading(true)
    try {
      const data = await adminService.getAllOrders()
      console.log('Loaded orders from API:', data) // Debug log
      setOrders(data || [])
    } catch (error) {
      console.error('Failed to load orders:', error)
      setOrders([])
    } finally {
      setLoading(false)
    }
  }

  const updateOrderStatus = async (orderId, newStatus) => {
    try {
      await adminService.updateOrderStatus(orderId, newStatus)
      setOrders(orders.map(order => 
        order.id === orderId ? { ...order, status: newStatus } : order
      ))
    } catch (error) {
      console.error('Failed to update order status:', error)
      alert('Failed to update order status')
    }
  }

  const refreshOrders = () => {
    loadOrders()
  }

  const getStatusColor = (status) => {
    switch (status.toLowerCase()) {
      case 'pending': return '#ffc107'
      case 'confirmed': return '#17a2b8'
      case 'preparing': return '#fd7e14'
      case 'ready': return '#20c997'
      case 'delivered': return '#28a745'
      case 'cancelled': return '#dc3545'
      default: return '#6c757d'
    }
  }

  const getOrderStats = () => {
    const totalOrders = orders.length
    const pendingOrders = orders.filter(order => order.status.toLowerCase() === 'pending').length
    const totalRevenue = orders.reduce((sum, order) => sum + order.totalAmount, 0)
    const avgOrderValue = totalOrders > 0 ? totalRevenue / totalOrders : 0

    return { totalOrders, pendingOrders, totalRevenue, avgOrderValue }
  }

  const stats = getOrderStats()

  if (loading) {
    return <div className="loading">Loading orders...</div>
  }

  return (
    <div className="order-manager">
      <div className="manager-header">
        <h2>Order Management</h2>
        <button className="btn-refresh" onClick={refreshOrders}>
          <i className="fas fa-sync-alt"></i> Refresh
        </button>
      </div>

      <div className="orders-stats">
        <div className="stat-card">
          <h3>{stats.totalOrders}</h3>
          <p>Total Orders</p>
        </div>
        <div className="stat-card">
          <h3>{stats.pendingOrders}</h3>
          <p>Pending Orders</p>
        </div>
        <div className="stat-card">
          <h3>${stats.totalRevenue.toFixed(2)}</h3>
          <p>Total Revenue</p>
        </div>
        <div className="stat-card">
          <h3>${stats.avgOrderValue.toFixed(2)}</h3>
          <p>Avg Order Value</p>
        </div>
      </div>

      {orders.length === 0 ? (
        <div className="no-orders">
          <i className="fas fa-receipt"></i>
          <h3>No orders found</h3>
          <p>Orders will appear here when customers place them.</p>
        </div>
      ) : (
        <div className="orders-list">
          {orders.map(order => (
            <div key={order.id} className="order-card">
              <div className="order-header">
                <div className="order-info">
                  <h3>Order #{order.id}</h3>
                  <p>
                    <i className="fas fa-user"></i> {order.customerName} 
                    <span className="email">({order.customerEmail})</span>
                    <span className="date">
                      <i className="fas fa-calendar"></i> 
                      {new Date(order.orderDate).toLocaleDateString()} {new Date(order.orderDate).toLocaleTimeString()}
                    </span>
                  </p>
                </div>
                <div className="order-status">
                  <span 
                    className="status-badge" 
                    style={{ backgroundColor: getStatusColor(order.status) }}
                  >
                    {order.status}
                  </span>
                  <select 
                    className="status-select"
                    value={order.status}
                    onChange={(e) => updateOrderStatus(order.id, e.target.value)}
                  >
                    <option value="Pending">Pending</option>
                    <option value="Confirmed">Confirmed</option>
                    <option value="Preparing">Preparing</option>
                    <option value="Ready">Ready</option>
                    <option value="Delivered">Delivered</option>
                    <option value="Cancelled">Cancelled</option>
                  </select>
                </div>
              </div>

              <div className="order-details">
                <div className="customer-details">
                  <h4>Customer Information</h4>
                  <p><i className="fas fa-phone"></i> {order.customerPhone}</p>
                  <p><i className="fas fa-map-marker-alt"></i> {order.deliveryAddress}</p>
                  <p><i className="fas fa-clock"></i> Est. Delivery: {new Date(order.estimatedDelivery).toLocaleTimeString()}</p>
                </div>
                <div className="order-summary">
                  <h4>Order Summary</h4>
                  <p><strong>Total: ${order.totalAmount.toFixed(2)}</strong></p>
                  <p>Items: {order.items?.length || 0}</p>
                </div>
              </div>

              <div className="order-items">
                <h4>Order Items</h4>
                <div className="items-list">
                  <div className="item-row" style={{ fontWeight: 'bold', borderBottom: '2px solid #ddd' }}>
                    <span>Pizza</span>
                    <span>Size</span>
                    <span>Qty</span>
                    <span>Price</span>
                  </div>
                  {order.items?.map((item, index) => (
                    <div key={index} className="item-row">
                      <span>{item.pizzaName}</span>
                      <span style={{ textTransform: 'capitalize' }}>{item.size}</span>
                      <span>{item.quantity}</span>
                      <span>${item.totalPrice.toFixed(2)}</span>
                    </div>
                  ))}
                </div>
                <div className="order-total">
                  <strong>Total: ${order.totalAmount.toFixed(2)}</strong>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

export default OrderManager