
import { About, Opleiding, Werkervaring, Getuigschrift, ProjectsDtScience } from './Data/Cvdata';


import React from 'react';
import Navbar from './components/Navbar';
import Footer from './components/Footer';
import CvMatcher from './components/CvMatcher';
import './App.css';

// Mouse follower animation
function MouseFollower() {
  React.useEffect(() => {
    const follower = document.createElement('div');
    follower.className = 'mouse-follower';
    document.body.appendChild(follower);
    const move = (e) => {
      follower.style.transform = `translate(${e.clientX - 16}px, ${e.clientY - 16}px)`;
    };
    window.addEventListener('mousemove', move);
    return () => {
      window.removeEventListener('mousemove', move);
      document.body.removeChild(follower);
    };
  }, []);
  return null;
}

const sections = [
  { label: 'About', id: 'about' },
  { label: 'Education', id: 'education' },
  { label: 'Work Experience', id: 'work' },
  { label: 'Certificates', id: 'certificates' },
  { label: 'Data Science Projects', id: 'projects' },
];

function Section({ title, id, children }) {
  return (
    <section id={id}>
      <h2>{title}</h2>
      {children}
    </section>
  );
}



function App() {
  return (
    <>
      <MouseFollower />
      <Navbar sections={sections} />
      <div className="hero">
        <div className="hero-intro">Hi, my name is</div>
        <h1>Fatna Eddaoudy</h1>
        <h2>Software Engineer</h2>
        <div className="hero-desc">
          I’m a Full Stack .NET Developer passionate about building robust, scalable web applications and solving real-world problems with code. I enjoy working at the intersection of backend development, frontend design, and data-driven thinking—creating solutions that are both efficient and user-friendly.
        </div>
      </div>
      <main>
        <Section title="About" id="about">
          {About.map((item, idx) => (
            <div key={idx}>
              <p>{item.description1}</p>
              <p>{item.description2}</p>
              <p>{item.description3}</p>
            </div>
          ))}
        </Section>
        <Section title="Education" id="education">
          {Opleiding.map((edu, idx) => (
            <div key={idx}>
              <strong>{edu.title}</strong> - {edu.school} ({edu.location})<br />
              <span>{edu.startYear} - {edu.endYear}</span>
              <ul>{edu.description.map((d, i) => <li key={i}>{d}</li>)}</ul>
              <div><b>Skills:</b> {edu.skills.join(', ')}</div>
            </div>
          ))}
        </Section>
        <Section title="Work Experience" id="work">
          {Werkervaring.map((job, idx) => (
            <div key={idx}>
              <strong>{job.role}</strong> - {job.company} ({job.location})<br />
              <span>{job.startDate} - {job.endDate}</span>
              <ul>{job.description.map((d, i) => <li key={i}>{d}</li>)}</ul>
              <div><b>Skills:</b> {job.skills.join(', ')}</div>
            </div>
          ))}
        </Section>
        <Section title="Certificates" id="certificates">
          {Getuigschrift.map((cert, idx) => (
            <div key={idx}>
              <strong>{cert.title}</strong> - {cert.school} ({cert.location})<br />
              <span>{cert.startYear} - {cert.endYear}</span>
              <ul>{cert.description.map((d, i) => <li key={i}>{d}</li>)}</ul>
              <div><b>Skills:</b> {cert.skills.join(', ')}</div>
            </div>
          ))}
        </Section>
        <Section title="Data Science Projects" id="projects">
          {ProjectsDtScience.map((proj, idx) => (
            <div key={idx}>
              <strong>{proj.title}</strong><br />
              <ul>{proj.description.map((d, i) => <li key={i}>{d}</li>)}</ul>
              <div><b>Skills:</b> {proj.skills.join(', ')}</div>
              <div><b>Image:</b> <i>{proj.foto}</i> (add image to public/ if available)</div>
            </div>
          ))}
        </Section>
        <Section title="CV Matcher" id="cv-matcher">
          <CvMatcher />
        </Section>
      </main>
      <Footer />
    </>
  );
}

export default App;
