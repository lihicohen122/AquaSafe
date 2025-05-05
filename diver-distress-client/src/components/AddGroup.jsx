import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import "./AddGroup.css";

export default function AddGroup() {
  const navigate = useNavigate();
  const [error, setError] = useState(null);
  const [formData, setFormData] = useState({
    name: "",
  });

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
    if (error) setError(null);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await axios.post("http://localhost:5000/groups", formData);
      navigate("/");
    } catch (error) {
      if (error.response?.status === 400) {
        setError("Group name already exists");
      } else {
        setError("Error creating group. Please try again.");
      }
      console.error("Failed to add group:", error);
    }
  };

  return (
    <div className="add-group-container">
      <div className="form-header">
        <h2>Add New Group</h2>
      </div>
      
      {error && (
        <div className="error-message">
          {error}
        </div>
      )}

      <form onSubmit={handleSubmit} className="group-form">
        <div className="form-group">
          <label htmlFor="name">Group Name</label>
          <input
            id="name"
            type="text"
            name="name"
            value={formData.name}
            onChange={handleChange}
            required
            placeholder="Enter group name"
          />
        </div>

        <div className="form-actions">
          <button type="submit" className="submit-btn">
            <span>Add Group</span>
          </button>
          <button 
            type="button" 
            className="cancel-btn"
            onClick={() => navigate("/")}
          >
            <span>Cancel</span>
          </button>
        </div>
      </form>
    </div>
  );
} 