import React, { useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import axios from "axios";
import "./AddDiver.css";

export default function AddDiver() {
  const { groupId } = useParams();
  const navigate = useNavigate();
  const [error, setError] = useState(null);

  const [formData, setFormData] = useState({
    id: "",
    name: "",
    age: "",
    weight: "",
    contact_info: "",
    bpm: "",
    entry_point: "",
    current_depth: "",
    status: "normal"
  });

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
    // Clear error when user starts typing
    if (error) setError(null);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const payload = { ...formData, group_id: parseInt(groupId) };
      await axios.post("http://localhost:5000/divers", payload);
      navigate(`/group/${groupId}`);
    } catch (error) {
      // Display the server's error message from the detail field
      setError(error.response?.data?.detail || "An error occurred");
      console.error("Failed to add diver:", error);
    }
  };

  const getInputType = (key) => {
    switch (key) {
      case 'age':
      case 'weight':
      case 'bpm':
      case 'current_depth':
        return 'number';
      default:
        return 'text';
    }
  };

  const getLabel = (key) => {
    const labels = {
      id: "ID Number",
      name: "Full Name",
      age: "Age",
      weight: "Weight (kg)",
      contact_info: "Contact Information",
      bpm: "Heart Rate (BPM)",
      entry_point: "Entry Point",
      current_depth: "Current Depth (meters)",
      status: "Status"
    };
    return labels[key] || key;
  };

  return (
    <div className="add-diver-container">
      <div className="form-header">
        <h2>Add New Diver</h2>
        <p className="group-info">Group {groupId}</p>
      </div>
      
      {error && (
        <div className="error-message">
          {error}
        </div>
      )}

      <form onSubmit={handleSubmit} className="diver-form">
        <div className="form-grid">
          {Object.keys(formData).map((key) => (
            key !== "status" ? (
              <div className="form-group" key={key}>
                <label htmlFor={key}>{getLabel(key)}</label>
                <input
                  id={key}
                  type={getInputType(key)}
                  name={key}
                  value={formData[key]}
                  onChange={handleChange}
                  required
                  placeholder={`Enter ${getLabel(key).toLowerCase()}`}
                />
              </div>
            ) : (
              <div className="form-group" key={key}>
                <label htmlFor={key}>{getLabel(key)}</label>
                <select
                  id={key}
                  name={key}
                  value={formData[key]}
                  onChange={handleChange}
                  className="status-select"
                >
                  <option value="normal">Normal</option>
                  <option value="warning">Warning</option>
                  <option value="critical">Critical</option>
                </select>
              </div>
            )
          ))}
        </div>

        <div className="form-actions">
          <button type="submit" className="submit-btn">
            <span>Add Diver</span>
          </button>
          <button 
            type="button" 
            className="cancel-btn"
            onClick={() => navigate(`/group/${groupId}`)}
          >
            <span>Cancel</span>
          </button>
        </div>
      </form>
    </div>
  );
}
