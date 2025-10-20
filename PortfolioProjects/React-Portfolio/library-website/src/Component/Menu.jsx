import { Link } from "react-router-dom";
import React, { useState } from "react";  // ✅ include useState
import SearchModal from "./SearchModal";

export default function Menu({ onSearch }) {
 const [isModalOpen, setIsModalOpen] = useState(false);
    return (

        <div className="main">
            <ul>
                <li> <a href="">Daschboard</a></li>
                <li><Link to="/books">Books</Link></li>
                 <li><Link to="/books">Search Book</Link></li>
                <li><a href="">Add Boek</a></li>
                <li><a href="">Return books</a></li>
                <li><a href="">Returned books history</a></li>
            </ul>
              <SearchModal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        onSearch={onSearch}
      />
        </div>
    );
}