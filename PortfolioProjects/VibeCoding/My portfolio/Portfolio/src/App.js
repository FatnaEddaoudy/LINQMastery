import React from 'react';
import './App.css';
import Header from './components/Header';
import About from './components/About';
import Education from './components/Education';
import Experience from './components/Experience';
import Certifications from './components/Certifications';
import Projects from './components/Projects';
import Footer from './components/Footer';
import BackToTop from './components/BackToTop';

function App() {
  return (
    <div className="App">
      <Header />
      <main>
        <About />
        <Education />
        <Experience />
        <Certifications />
        <Projects />
      </main>
      <Footer />
      <BackToTop />
    </div>
  );
}

export default App;