import React, { useState } from 'react';
import { ProjectsDtScience, ProjectsAdditional, ProjectsVibeCoding } from '../data/CVdata';

const Projects = () => {
  const [activeTab, setActiveTab] = useState('data-science');

  const allProjects = {
    'data-science': ProjectsDtScience,
    'additional': ProjectsAdditional,
    'vibe-coding': ProjectsVibeCoding
  };

  return (
    <section id="projects" className="section projects-section">
      <div className="container">
        <h2 className="section-title">Projects</h2>
        <p className="section-subtitle">
          Beyond core development, my recent certification in Data Science and active projects highlight my eagerness to integrate analytical technology.
        </p>
        
        <div className="projects-tabs">
          <button 
            className={`tab-button ${activeTab === 'data-science' ? 'active' : ''}`}
            onClick={() => setActiveTab('data-science')}
          >
            🤖 Data Science Projects
          </button>
          <button 
            className={`tab-button ${activeTab === 'additional' ? 'active' : ''}`}
            onClick={() => setActiveTab('additional')}
          >
            💻 .NET Projects
          </button>
          <button 
            className={`tab-button ${activeTab === 'vibe-coding' ? 'active' : ''}`}
            onClick={() => setActiveTab('vibe-coding')}
          >
            🚀 Vibe Coding Projects
          </button>
        </div>

        <div className="projects-grid">
          {allProjects[activeTab].map((project, index) => (
            <div key={index} className="project-card">
              <div className="project-header">
                <h3 className="project-title">{project.title}</h3>
                <div className="project-links">
                  <a 
                    href={project.githubLink} 
                    target="_blank" 
                    rel="noopener noreferrer" 
                    className="project-link github-link"
                    title="View on GitHub"
                  >
                    🐙 GitHub
                  </a>
                  {project.demoLink && (
                    <a 
                      href={project.demoLink} 
                      target="_blank" 
                      rel="noopener noreferrer" 
                      className="project-link demo-link"
                      title="Live Demo"
                    >
                      🔗 Demo
                    </a>
                  )}
                </div>
              </div>
              
              <div className="project-description">
                {project.description.map((desc, descIndex) => (
                  <p key={descIndex}>{desc}</p>
                ))}
              </div>
              
              <div className="project-skills">
                <h5>Technologies Used:</h5>
                <div className="skills-list">
                  {project.skills.map((skill, skillIndex) => (
                    <span key={skillIndex} className="skill-tag project-skill">{skill}</span>
                  ))}
                </div>
              </div>
              
              <div className="project-footer">
                <a 
                  href={project.githubLink} 
                  target="_blank" 
                  rel="noopener noreferrer" 
                  className="btn-primary project-btn"
                >
                  🐙 View Code
                </a>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default Projects;