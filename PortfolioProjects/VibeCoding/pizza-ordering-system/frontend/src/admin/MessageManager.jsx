import React, { useState, useEffect } from 'react'
import { adminService } from '../services/adminService'

const MessageManager = () => {
  const [messages, setMessages] = useState([])
  const [loading, setLoading] = useState(true)
  const [filter, setFilter] = useState('all') // all, unread, read
  const [replyModal, setReplyModal] = useState({ isOpen: false, message: null })
  const [replyText, setReplyText] = useState('')
  const [isSending, setIsSending] = useState(false)

  useEffect(() => {
    loadMessages()
  }, [])

  const loadMessages = async () => {
    setLoading(true)
    try {
      const data = await adminService.getAllMessages()
      console.log('Loaded messages from API:', data) // Debug log
      setMessages(data || [])
    } catch (error) {
      console.error('Failed to load messages:', error)
      setMessages([])
    } finally {
      setLoading(false)
    }
  }

  const markAsRead = async (messageId) => {
    try {
      await adminService.markMessageAsRead(messageId)
      setMessages(messages.map(msg => 
        msg.id === messageId ? { ...msg, isRead: true } : msg
      ))
    } catch (error) {
      console.error('Error marking message as read:', error)
      alert('Failed to mark message as read')
    }
  }

  const deleteMessage = (messageId) => {
    if (confirm('Are you sure you want to delete this message?')) {
      setMessages(messages.filter(msg => msg.id !== messageId))
      alert('Message deleted (demo mode)')
    }
  }

  const openReplyModal = (message) => {
    setReplyModal({ isOpen: true, message })
    setReplyText(`Hi ${message.name},\n\nThank you for contacting Tony's Pizza!\n\n`)
  }

  const closeReplyModal = () => {
    setReplyModal({ isOpen: false, message: null })
    setReplyText('')
  }

  const sendReply = async (e) => {
    e.preventDefault()
    if (!replyText.trim()) {
      alert('Please enter a reply message')
      return
    }

    setIsSending(true)
    try {
      // Send reply via API
      await adminService.replyToMessage(replyModal.message.id, replyText)
      
      // Mark message as read
      markAsRead(replyModal.message.id)
      
      alert('Reply sent successfully to the customer\'s Gmail!')
      closeReplyModal()
    } catch (error) {
      console.error('Failed to send reply:', error)
      alert('Failed to send reply. Please try again.')
    } finally {
      setIsSending(false)
    }
  }

  const formatDate = (date) => {
    return new Date(date).toLocaleString()
  }

  const filteredMessages = messages.filter(msg => {
    if (filter === 'unread') return !msg.isRead
    if (filter === 'read') return msg.isRead
    return true // all
  })

  const unreadCount = messages.filter(msg => !msg.isRead).length

  if (loading) {
    return <div className="loading">Loading messages...</div>
  }

  return (
    <div className="message-manager">
      <div className="manager-header">
        <h2><i className="fas fa-envelope"></i> Contact Messages</h2>
        <button className="btn-refresh" onClick={loadMessages}>
          <i className="fas fa-sync-alt"></i> Refresh
        </button>
      </div>

      <div className="email-status" style={{
        background: '#d4edda',
        border: '1px solid #c3e6cb',
        borderRadius: '5px',
        padding: '10px',
        margin: '10px 0',
        color: '#155724'
      }}>
        <i className="fas fa-check-circle"></i> <strong>Email Configured:</strong> Gmail SMTP enabled. 
        Replies will be sent to customer email addresses.
      </div>

      <div className="message-stats">
        <div className="stat-card">
          <h3>{messages.length}</h3>
          <p>Total Messages</p>
        </div>
        <div className="stat-card">
          <h3>{unreadCount}</h3>
          <p>Unread</p>
        </div>
        <div className="stat-card">
          <h3>{messages.filter(m => m.isRead).length}</h3>
          <p>Read</p>
        </div>
      </div>

      <div className="message-filters">
        <button 
          className={`filter-btn ${filter === 'all' ? 'active' : ''}`}
          onClick={() => setFilter('all')}
        >
          All Messages ({messages.length})
        </button>
        <button 
          className={`filter-btn ${filter === 'unread' ? 'active' : ''}`}
          onClick={() => setFilter('unread')}
        >
          Unread ({unreadCount})
        </button>
        <button 
          className={`filter-btn ${filter === 'read' ? 'active' : ''}`}
          onClick={() => setFilter('read')}
        >
          Read ({messages.filter(m => m.isRead).length})
        </button>
      </div>

      <div className="messages-list">
        {filteredMessages.length === 0 ? (
          <div className="no-messages">
            <i className="fas fa-envelope-open"></i>
            <p>No messages found</p>
          </div>
        ) : (
          filteredMessages.map(message => (
            <div 
              key={message.id} 
              className={`message-card ${!message.isRead ? 'unread' : ''}`}
            >
              <div className="message-header">
                <div className="message-info">
                  <h3>{message.name}</h3>
                  <span className="email">{message.email}</span>
                  <span className="date">{formatDate(message.createdAt)}</span>
                </div>
                <div className="message-status">
                  {!message.isRead && <span className="unread-badge">New</span>}
                </div>
              </div>

              <div className="message-content">
                <p>{message.message}</p>
              </div>

              <div className="message-actions">
                {!message.isRead && (
                  <button 
                    className="btn-mark-read"
                    onClick={() => markAsRead(message.id)}
                  >
                    <i className="fas fa-check"></i> Mark as Read
                  </button>
                )}
                <button 
                  className="btn-reply"
                  onClick={() => openReplyModal(message)}
                >
                  <i className="fas fa-reply"></i> Reply
                </button>
                <button 
                  className="btn-delete"
                  onClick={() => deleteMessage(message.id)}
                >
                  <i className="fas fa-trash"></i> Delete
                </button>
              </div>
            </div>
          ))
        )}
      </div>

      {/* Reply Modal */}
      {replyModal.isOpen && (
        <div className="modal-overlay" onClick={closeReplyModal}>
          <div className="reply-modal" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h3>Reply to {replyModal.message.name}</h3>
              <button className="close-modal" onClick={closeReplyModal}>
                <i className="fas fa-times"></i>
              </button>
            </div>
            
            <div className="modal-body">
              <div className="original-message">
                <h4>Original Message:</h4>
                <p><strong>From:</strong> {replyModal.message.name} ({replyModal.message.email})</p>
                <p><strong>Date:</strong> {formatDate(replyModal.message.createdAt)}</p>
                <p><strong>Message:</strong></p>
                <div className="original-text">{replyModal.message.message}</div>
              </div>
              
              <form onSubmit={sendReply}>
                <div className="form-group">
                  <label>Your Reply:</label>
                  <textarea
                    value={replyText}
                    onChange={(e) => setReplyText(e.target.value)}
                    placeholder="Type your reply here..."
                    rows="8"
                    required
                  />
                </div>
                
                <div className="modal-actions">
                  <button type="button" className="btn-cancel" onClick={closeReplyModal}>
                    Cancel
                  </button>
                  <button type="submit" className="btn-send" disabled={isSending}>
                    {isSending ? 'Sending...' : 'Send Reply'}
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default MessageManager