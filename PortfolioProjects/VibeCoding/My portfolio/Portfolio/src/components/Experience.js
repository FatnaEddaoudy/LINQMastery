import React from 'react';
import { Werkervaring } from '../data/CVdata';

const Experience = () => {
  return (
    <section id="experience" className="section experience-section">
      <div className="container">
        <h2 className="section-title">Work Experience</h2>
        <div className="experience-timeline">
          {Werkervaring.map((work, index) => (
            <div key={index} className="experience-card">
              <div className="experience-header">
                <span className="experience-icon">💼</span>
                <div className="experience-info">
                  <h3 className="experience-role">{work.role}</h3>
                  <h4 className="experience-company">{work.company}</h4>
                  <div className="experience-meta">
                    <span className="experience-location">
                      📍 {work.location}
                    </span>
                    <span className="experience-period">
                      📅 {work.startDate} - {work.endDate}
                    </span>
                  </div>
                </div>
              </div>
              
              <div className="experience-description">
                <ul>
                  {work.description.map((desc, descIndex) => (
                    <li key={descIndex}>{desc}</li>
                  ))}
                </ul>
              </div>
              
              <div className="skills-container">
                <h5>Skills & Technologies:</h5>
                <div className="skills-list">
                  {work.skills.map((skill, skillIndex) => (
                    <span key={skillIndex} className="skill-tag">{skill}</span>
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

export default Experience;