import logo from './logo.svg';
import './index.css';
import Book from '../src/Component/Book'
import Menu from './Component/Menu';
import Menuright from './Component/Menuright';
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

function App() {
  return (
    
       <Router>
    <div className="app">
      <header className="header">
        <h1>📚 Library Management System</h1>
      </header>

      <div className="container">
        <aside className="left-menu">
          <Menu />
        </aside>

        <main className="content">
           <Routes>
          <Route path="/books" element={<Book />} />
          </Routes>
        </main>

        <aside className="right-menu">
          <Menuright />
        </aside>
      </div>

      <footer className="footer">
        <p>&copy; 2025 Library System</p>
      </footer>

      
   

    </div>
     </Router>
  );
};


export default App;
