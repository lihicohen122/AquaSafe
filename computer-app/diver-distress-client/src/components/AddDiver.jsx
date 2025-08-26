import React, { useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import axios from "axios";
import "./AddDiver.css";

export default function AddDiver() {
  const { groupId } = useParams();
  const navigate = useNavigate();

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

  const [error, setError] = useState("");

  const validateId = (id) => {
    return /^[a-zA-Z]+$/.test(id);
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    
    if (name === "id") {
      if (value === "" || validateId(value)) {
        setFormData({ ...formData, [name]: value });
        setError("");
      } else {
        setError("ID must contain only letters");
      }
    } else {
      setFormData({ ...formData, [name]: value });
    }
  };

  const validateForm = () => {
    if (!validateId(formData.id)) {
      setError("ID must contain only letters");
      return false;
    }
    
    // Validate numeric fields
    if (isNaN(formData.age) || formData.age === "") {
      setError("Age must be a valid number");
      return false;
    }
    
    if (isNaN(formData.weight) || formData.weight === "") {
      setError("Weight must be a valid number");
      return false;
    }
    
    if (isNaN(formData.bpm) || formData.bpm === "") {
      setError("BPM must be a valid number");
      return false;
    }
    
    if (isNaN(formData.current_depth) || formData.current_depth === "") {
      setError("Current depth must be a valid number");
      return false;
    }
    
    return true;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!validateForm()) {
      return;
    }

    try {
      const diverInfo = {
        ...formData,
        age: parseInt(formData.age),
        weight: parseFloat(formData.weight),
        bpm: parseInt(formData.bpm),
        current_depth: parseFloat(formData.current_depth),
        group_id: parseInt(groupId)
      };
      
      await axios.post("http://localhost:5000/divers/web", diverInfo);
      navigate(`/group/${groupId}`);
    } catch (error) {
      console.error("Failed to add diver:", error);
      if (error.response) {
        setError(error.response.data.detail || "Failed to add diver. Please check your input.");
      } else {
        setError("Failed to connect to server");
      }
    }
  };

  return (
    <div className="add-diver-container">
      <h2>Add New Diver to Group {groupId}</h2>
      {error && <div className="error-message">{error}</div>}
      <form onSubmit={handleSubmit} className="diver-form">
        {Object.keys(formData).map((key) => {
          if (key === "status") return null;
          
          let inputProps = {
            type: "text",
            key,
            name: key,
            placeholder: key.replace("_", " "),
            value: formData[key],
            onChange: handleChange,
            required: true
          };

          if (["age", "bpm"].includes(key)) {
            inputProps.type = "number";
          } else if (["weight", "current_depth"].includes(key)) {
            inputProps.type = "number";
            inputProps.step = "0.01";
          }
          
          return <input {...inputProps} />;
        })}
        <select name="status" value={formData.status} onChange={handleChange}>
          <option value="normal">Normal</option>
          <option value="warning">Warning</option>
          <option value="critical">Critical</option>
        </select>
        <button type="submit">Add Diver</button>
      </form>
      <button onClick={() => navigate(`/group/${groupId}`)}>Cancel</button>
    </div>
  );
}
