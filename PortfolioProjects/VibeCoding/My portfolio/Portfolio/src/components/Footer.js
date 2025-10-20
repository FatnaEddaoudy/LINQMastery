import React from 'react';
import { PersonalInfo } from '../data/CVdata';

const Footer = () => {
  return (
    <footer className="footer">
      <div className="container">
        <div className="footer-content">
          <div className="footer-info">
            <h3>{PersonalInfo.name}</h3>
            <p>{PersonalInfo.title}</p>
            <p>Building the future, one line of code at a time.</p>
          </div>
          
          <div className="footer-links">
            <h4>Connect</h4>
            <div className="social-links">
              <a href={PersonalInfo.linkedin} target="_blank" rel="noopener noreferrer" className="social-link">
                💼 LinkedIn
              </a>
              <a href={PersonalInfo.github} target="_blank" rel="noopener noreferrer" className="social-link">
                🐙 GitHub
              </a>
              <a href={`mailto:${PersonalInfo.email}`} className="social-link">
                ✉️ Email
              </a>
            </div>
          </div>
        </div>
        
        <div className="footer-bottom">
          <p>
            © {new Date().getFullYear()} {PersonalInfo.name}. Made with ❤️ and React.
          </p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;