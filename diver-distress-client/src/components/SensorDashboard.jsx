import React, { useEffect, useState } from "react";
import axios from "axios";
import { useNavigate, Link } from 'react-router-dom';
import '../styles/GlobalStyles.css';
import "./SensorDashboard.css"; // CSS file for design 

//exporting this page
export default function SensorDashboard() {
  const [sensors, setSensors] = useState([]);
  const navigate = useNavigate();

  //connecting the server to this page
  useEffect(() => {
    axios.get("http://localhost:5000/sensors")
      .then(response => setSensors(response.data))
      .catch(error => console.error("Error fetching sensors:", error));
  }, []);

  //get the users status from server
  //if someone is critical we will like to get his details for the alert box 
  const criticalSensor = sensors.find(s => s.status === "critical");

  const getStatusClass = (status) => {
    switch (status) {
      case "normal": return "sensor normal";
      case "warning": return "sensor warning";
      case "critical": return "sensor critical";
      default: return "sensor";
    }
  };

  return (
    <div className="dashboard">
      <button className="back-button" onClick={() => navigate('/')}>Back to My Groups</button>
      {/* The alert box */}
      <div className="alert-box">
        <h2>Alert:</h2>
        {criticalSensor ? (
          <div className="alert-text">
            🔴 DIVER #{criticalSensor.id} IS IN CRITICAL STATE- BPM {criticalSensor.bpm}
          </div>
        ) : (
          <p>No Current Alerts</p>
        )}
      </div>
      
      {/* This is the box for each diver (no matter his status) */}
      <div className="sensor-grid">
        {sensors.map(sensor => (
          <div key={sensor.id} className={getStatusClass(sensor.status)}>
            <span className="status-icon">
                {sensor.status === "normal" && "✔️"}
                {sensor.status === "warning" && "⚠️"}
                 {sensor.status === "critical" && "🔴"}
            </span>
            <div className="sensor-header">
              <Link to={`/diver/${sensor.id}`}>diver: {sensor.id}</Link>
            </div>

            <div className="sensor-info">
              <p>heartbeat: {sensor.bpm}</p>
              <p>current depth: {sensor.current_depth} meters</p> {/* שימוש ב-current_depth */}
              <p>status: {sensor.status === "normal" ? "Normal" : sensor.status === "warning" ? "Warning" : "CRITICAL"}</p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
