import React from 'react';
import { About as AboutData } from '../data/CVdata';

const About = () => {
  const aboutInfo = AboutData[0];

  return (
    <section id="about" className="section about-section">
      <div className="container">
        <h2 className="section-title">About Me</h2>
        <div className="about-content">
          <div className="about-text">
            <p className="about-paragraph">{aboutInfo.description1}</p>
            <p className="about-paragraph">{aboutInfo.description2}</p>
            <p className="about-paragraph">{aboutInfo.description3}</p>
          </div>
        </div>
      </div>
    </section>
  );
};

export default About;