import React, { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import axios from "axios";
import "../styles/GlobalStyles.css";
import "./DiverDetails.css";

export default function DiverDetails() {
  const { diverId } = useParams();
  const navigate = useNavigate();
  const [diver, setDiver] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    console.log("Fetching diver details for ID:", diverId.trim()); // בדיקת ה-id
    axios.get(`http://localhost:5000/divers/${diverId.trim()}`)
      .then(response => {
        console.log("Diver details fetched:", response.data); // בדיקת התגובה
        setDiver(response.data);
      })
      .catch(error => {
        console.error("Error fetching diver details:", error);
        setError("Failed to fetch diver details. Please try again later.");
      });
  }, [diverId]);

  if (error) {
    return <p>{error}</p>;
  }

  if (!diver) {
    return <p>Loading...</p>;
  }

  return (
    <div className="diver-details">
      <button className="back-button" onClick={() => navigate(-1)}>Back</button>
      <h2>Diver Details</h2>
      <p><strong>Name:</strong> {diver.name}</p>
      <p><strong>Age:</strong> {diver.age}</p>
      <p><strong>Weight:</strong> {diver.weight} kg</p>
      <p><strong>Contact Info:</strong> {diver.contact_info}</p>
      <p><strong>Heartbeat:</strong> {diver.bpm} bpm</p>
      <p><strong>Entry Point:</strong> {diver.entry_point}</p>
      <p><strong>Current Depth:</strong> {diver.current_depth} meters</p>
      <p><strong>Status:</strong> {diver.status}</p>
    </div>
  );
}