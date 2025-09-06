import React, { useEffect, useState } from "react";
import axios from "axios";
import { useNavigate, Link, useParams } from 'react-router-dom';
import '../../../../../styles/GlobalStyles.css';
import "./SensorDashboard.css";

//exporting this page
export default function SensorDashboard() {
  const [divers, setDivers] = useState([]);
  const navigate = useNavigate();
  const { groupId } = useParams();

  //connecting the server to this page
  useEffect(() => {
    axios.get(`http://localhost:5000/groups/${groupId}`)
      .then(response => {
        console.log("Group response:", response.data);
        if (response.data.divers) {
          setDivers(response.data.divers);
        } else {
          console.warn("No 'divers' field in group response");
          setDivers([]);
        }
      })
      .catch(error => console.error("Error fetching group with divers:", error));
  }, [groupId]);

  //get the users status from server
  //if someone is critical we will like to get his details for the alert box 
  const criticalDiver = divers.find(s => s.status === "critical");
  const warningDiver = divers.find(s => s.status === "warning");

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
        <h2>Alert:</h2>
        {criticalDiver ? (
          <div className="alert-text">
            🆘 DIVER #{criticalDiver.id} IS IN CRITICAL STATE- BPM {criticalDiver.bpm}
          </div>
        ) : (
          <p>No Current Alerts</p>
        )}
        {warningDiver && (
          <div className="alert-text warning">
            ⚠️ DIVER #{warningDiver.id} IS IN WARNING STATE - BPM {warningDiver.bpm}
          </div>
        )}
      </div>

      {/* This is the box for each diver (no matter his status) */}
      <div className="sensor-grid">
        {divers.map(diver => (
          <div key={diver.id} className={getStatusClass(diver.status)}>
            <span className="status-icon">
              {diver.status === "normal" && "✅"}
              {diver.status === "warning" && "⚠️"}
              {diver.status === "critical" && "🆘"}
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
