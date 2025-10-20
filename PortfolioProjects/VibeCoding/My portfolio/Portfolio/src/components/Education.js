import React from 'react';
import { Opleiding } from '../data/CVdata';

const Education = () => {
  return (
    <section id="education" className="section education-section">
      <div className="container">
        <h2 className="section-title">Education</h2>
        <div className="education-grid">
          {Opleiding.map((education, index) => (
            <div key={index} className="education-card">
              <div className="education-header">
                <span className="education-icon">🎓</span>
                <div className="education-info">
                  <h3 className="education-title">{education.title}</h3>
                  <h4 className="education-school">{education.school}</h4>
                  <div className="education-meta">
                    <span className="education-location">
                      📍 {education.location}
                    </span>
                    <span className="education-period">
                      {education.startYear} - {education.endYear}
                    </span>
                  </div>
                </div>
              </div>
              
              <div className="education-description">
                {education.description.map((desc, descIndex) => (
                  <p key={descIndex}>{desc}</p>
                ))}
              </div>
              
              <div className="skills-container">
                <h5>Skills & Technologies:</h5>
                <div className="skills-list">
                  {education.skills.map((skill, skillIndex) => (
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

export default Education;