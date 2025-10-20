import'./index.css';
import Menu from './Components/Menu';
import Home from'./Components/Home';
import Opleiding from './Components/Opleiding';
import Projecten from './Components/Projecten';
import Conatct from './Components/Contact';

import {
  getAbout,
  getOpleiding,
  getWerkervaring,
  getGetuigschrift,
  getProjects,
 
} from "./Services/ProfileService";


function App() {

  return (
    <div className='container'>
        <div className="main">
          <div className="menu">
             <Menu/>
          </div>
      </div>

        <div className='inhoud'>
        <Home Aboutinfo={getAbout()}/>
        <Opleiding OpleingLijst={getOpleiding()}/>
        <Projecten ProjectenLijst={getProjects()}/>
        <Conatct/>

        </div>
    </div>
  );
}
export default App;
