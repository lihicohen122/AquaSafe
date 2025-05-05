import React, { useEffect, useState } from "react";
import axios from "axios";
import { useNavigate, Link, useParams } from 'react-router-dom';
import '../styles/GlobalStyles.css';
import "./SensorDashboard.css"; // CSS file for design 

//exporting this page
export default function SensorDashboard() {
  const [divers, setDivers] = useState([]);
  const navigate = useNavigate();
  const { groupId } = useParams();

  //connecting the server to this page
  useEffect(() => {
    axios.get(`http://localhost:5000/groups/${groupId}`)
      .then(response => {
        console.log("Group response:", response.data); // 🟡 חשוב!
        if (response.data.divers) {
          setDivers(response.data.divers);
        } else {
          console.warn("No 'divers' field in group response");
          setDivers([]);
        }
      })
      .catch(error => console.error("Error fetching group with divers:", error));
  }, [groupId]);

  // Get all critical and warning divers
  const criticalDivers = divers.filter(diver => diver.status === "critical");
  const warningDivers = divers.filter(diver => diver.status === "warning");

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

      {/* The alert box */}
      <div className="alert-box">
        <h2>Alerts:</h2>
        <div className="alerts-container">
          {criticalDivers.length > 0 ? (
            <div className="critical-alerts">
              {criticalDivers.map(diver => (
                <div key={diver.id} className="alert-text critical">
                  🔴 DIVER #{diver.id} IS IN CRITICAL STATE - BPM {diver.bpm}
                </div>
              ))}
            </div>
          ) : null}
          
          {warningDivers.length > 0 ? (
            <div className="warning-alerts">
              {warningDivers.map(diver => (
                <div key={diver.id} className="alert-text warning">
                  ⚠️ DIVER #{diver.id} IS IN WARNING STATE - BPM {diver.bpm}
                </div>
              ))}
            </div>
          ) : null}
          
          {criticalDivers.length === 0 && warningDivers.length === 0 && (
            <p>No Current Alerts</p>
          )}
        </div>
      </div>

      {/* This is the box for each diver (no matter his status) */}
      <div className="sensor-grid">
        {divers.map(diver => (
          <div key={diver.id} className={getStatusClass(diver.status)}>
            <span className="status-icon">
              {diver.status === "normal" && "✔️"}
              {diver.status === "warning" && "⚠️"}
              {diver.status === "critical" && "🔴"}
            </span>
            <div className="sensor-header">
              <Link to={`/diver/${diver.id}`}>Diver: {diver.id}</Link>
            </div>

            <div className="sensor-info">
              <p>heartbeat: {diver.bpm}</p>
              <p>current depth: {diver.current_depth} meters</p>
              <p>status: {diver.status === "normal" ? "Normal" : diver.status === "warning" ? "Warning" : "CRITICAL"}</p>
            </div>
          </div>
        ))}
      </div>

      <div className="dashboard-controls">
        <button className="add-diver-button" onClick={() => navigate(`/add-diver/${groupId}`)}>➕ Add Diver</button>
        <button className="delete-diver-button" onClick={() => navigate(`/delete-diver/${groupId}`)}>🗑️ Delete Diver</button>
      </div>
      <button className="add-group-button" onClick={() => navigate('/')}>Back to My Groups</button>

    </div>
  );
}
