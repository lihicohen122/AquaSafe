import React from 'react';
import { Link } from 'react-router-dom';
import './NavigationBar.css';
import logo from '../../images/Aquasafe Logo.jpeg';

const NavigationBar = () => {
  return (
    <nav className="navigation-bar">
      <div className="nav-logo">
        <img src={logo} alt="AquaSafe Logo" />
      </div>
      <ul>
        <li><Link to="/">Home</Link></li>
        <li><Link to="/about">About</Link></li>
        <li><Link to="/settings">Settings</Link></li>
        <li><Link to="/help">Help</Link></li>
      </ul>
    </nav>
  );
};

export default NavigationBar;