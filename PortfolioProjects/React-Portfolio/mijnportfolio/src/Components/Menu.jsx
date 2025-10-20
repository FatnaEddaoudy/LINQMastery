import React from "react";

export default function Menu(){

    return(
        <ul>
        <li><a href="#"><img src="./images/house.png" className="icone" alt="Home"/>  Home</a></li>
        <li><a href="#"><img src="./images/graduation.png" className="icone"  alt="Opleiding"/>  Opleiding en Education</a></li>
        <li><a href="#"><img src="./images/idea.png"  className="icone"  alt="Projecten"/>  Projecten</a></li>
        <li><a href="#"> <img src="./images/contact.png" className="icone"  alt="Contact"/>  Contact  </a></li>
        </ul>
    );
}