import React from 'react';


const Navbar = ({ sections }) => {
  return (
    <nav className="navbar-vertical-left">
      <ul>
        {sections.map((section) => (
          <li key={section.id}>
            <a href={`#${section.id}`}>{section.label}</a>
          </li>
        ))}
      </ul>
    </nav>
  );
};

export default Navbar;
