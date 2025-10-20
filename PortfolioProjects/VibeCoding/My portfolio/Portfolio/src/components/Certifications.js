import React from 'react';
import { Getuigschrift } from '../data/CVdata';

const Certifications = () => {
  return (
    <section id="certifications" className="section certifications-section">
      <div className="container">
        <h2 className="section-title">Certifications</h2>
        <div className="certifications-grid">
          {Getuigschrift.map((cert, index) => (
            <div key={index} className="certification-card">
              <div className="certification-header">
                <span className="certification-icon">🏆</span>
                <div className="certification-info">
                  <h3 className="certification-title">{cert.title}</h3>
                  <h4 className="certification-school">{cert.school}</h4>
                  <div className="certification-meta">
                    <span className="certification-location">
                      📍 {cert.location}
                    </span>
                    <span className="certification-period">
                      {cert.startYear} - {cert.endYear}
                    </span>
                  </div>
                </div>
              </div>
              
              <div className="certification-description">
                {cert.description.map((desc, descIndex) => (
                  <p key={descIndex}>{desc}</p>
                ))}
              </div>
              
              <div className="skills-container">
                <h5>Areas of Expertise:</h5>
                <div className="skills-list">
                  {cert.skills.map((skill, skillIndex) => (
                    <span key={skillIndex} className="skill-tag certification-skill">{skill}</span>
                  ))}
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default Certifications;