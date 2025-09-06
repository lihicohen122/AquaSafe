import React, { useState, useEffect } from "react";
import "./Settings.css";

export default function Settings() {
  // State for theme settings
  const [theme, setTheme] = useState('ocean'); // default theme

  // Load settings from localStorage on component mount
  useEffect(() => {
    const savedTheme = localStorage.getItem('theme') || 'ocean';
    
    setTheme(savedTheme);
    
    // Apply theme to document
    applyTheme(savedTheme);
  }, []);

  // Apply theme changes to the document
  const applyTheme = (selectedTheme) => {
    const root = document.documentElement;
    
    // Remove existing theme classes
    root.classList.remove('theme-ocean', 'theme-coral', 'theme-deep', 'dark-mode');
    
    // Add new theme class
    root.classList.add(`theme-${selectedTheme}`);
  };

  // Handle theme change
  const handleThemeChange = (newTheme) => {
    setTheme(newTheme);
    localStorage.setItem('theme', newTheme);
    applyTheme(newTheme);
  };

  return (
    <div className="settings-container">
      <h2>⚙️ Settings</h2>
      
      <div className="settings-section">
        <h3>🎨 Appearance</h3>
        
        {/* Theme Selection */}
        <div className="setting-item">
          <div className="setting-info">
            <strong>Color Theme</strong>
            <p>Choose your preferred color scheme</p>
          </div>
          <div className="theme-options">
            <button
              className={`theme-button theme-ocean ${theme === 'ocean' ? 'active' : ''}`}
              onClick={() => handleThemeChange('ocean')}
            >
              🌊 Ocean Blue
            </button>
            <button
              className={`theme-button theme-coral ${theme === 'coral' ? 'active' : ''}`}
              onClick={() => handleThemeChange('coral')}
            >
              🪸 Coral Reef
            </button>
            <button
              className={`theme-button theme-deep ${theme === 'deep' ? 'active' : ''}`}
              onClick={() => handleThemeChange('deep')}
            >
              🌚 Deep Sea
            </button>
          </div>
        </div>
      </div>

      <div className="settings-section">
        <h3>ℹ️ About Themes</h3>
        <div className="theme-info">
          <p><strong>Ocean Blue:</strong> Classic aqua colors for a fresh underwater feel</p>
          <p><strong>Coral Reef:</strong> Warm oranges and corals for a tropical vibe</p>
          <p><strong>Deep Sea:</strong> Dark blues and purples for deep water exploration</p>
        </div>
      </div>

      <div className="settings-footer">
        <p>Settings are automatically saved</p>
      </div>
    </div>
  );
}
