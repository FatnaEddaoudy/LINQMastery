function SearchModal({ isOpen, onClose, onSearch }) {
  if (!isOpen) return null; // don't render if closed

  return (
    <div className="modal-overlay">
      <div className="modal-content">
        <h3>Search Book</h3>
        <input
          type="text"
          placeholder="Type title or ISBN..."
          onChange={(e) => onSearch(e.target.value)}
        />
        <button onClick={onClose}>Close</button>
      </div>
    </div>
  );
}

export default SearchModal;
