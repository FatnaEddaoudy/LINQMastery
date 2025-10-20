import React from 'react';
import { PersonalInfo } from '../data/CVdata';

const Header = () => {
  const handleResumeDownload = () => {
    // This would typically trigger a download of the resume file
    const link = document.createElement('a');
    link.href = `/resume/${PersonalInfo.resumeFile}`;
    link.download = PersonalInfo.resumeFile;
    link.click();
  };

  const scrollToSection = (sectionId) => {
    const element = document.getElementById(sectionId);
    if (element) {
      element.scrollIntoView({ behavior: 'smooth' });
    }
  };

  return (
    <header className="header">
      <nav className="navbar">
        <div className="nav-brand">
          <h2>{PersonalInfo.name}</h2>
        </div>
        <ul className="nav-links">
          <li><a href="#about" onClick={() => scrollToSection('about')}>About</a></li>
          <li><a href="#education" onClick={() => scrollToSection('education')}>Education</a></li>
          <li><a href="#experience" onClick={() => scrollToSection('experience')}>Experience</a></li>
          <li><a href="#certifications" onClick={() => scrollToSection('certifications')}>Certifications</a></li>
          <li><a href="#projects" onClick={() => scrollToSection('projects')}>Projects</a></li>
        </ul>
        <button className="resume-btn" onClick={handleResumeDownload}>
          📄 Download Resume
        </button>
      </nav>
      
      <div className="hero-section">
        <div className="hero-content">
          <h1>{PersonalInfo.name}</h1>
          <h2 className="hero-title">{PersonalInfo.title}</h2>
          <p className="hero-description">
            Passionate about building robust, scalable web applications and solving real-world problems with code.
          </p>
          
          <div className="contact-info">
            <div className="contact-item">
              <span>✉️</span>
              <a href={`mailto:${PersonalInfo.email}`}>{PersonalInfo.email}</a>
            </div>
            <div className="contact-item">
              <span>📞</span>
              <span>{PersonalInfo.phone}</span>
            </div>
            <div className="contact-item">
              <span>📍</span>
              <span>{PersonalInfo.location}</span>
            </div>
          </div>
          
          <div className="social-links">
            <a href={PersonalInfo.linkedin} target="_blank" rel="noopener noreferrer" className="social-link">
              💼 LinkedIn
            </a>
            <a href={PersonalInfo.github} target="_blank" rel="noopener noreferrer" className="social-link">
              🐙 GitHub
            </a>
          </div>
          
          <div className="hero-actions">
            <button className="btn-primary" onClick={handleResumeDownload}>
              📄 Download Resume
            </button>
            <button className="btn-secondary" onClick={() => scrollToSection('about')}>
              Learn More
            </button>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;