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

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const payload = { ...formData, group_id: parseInt(groupId) };
      await axios.post("http://localhost:5000/divers", payload);
      navigate(`/group/${groupId}`);
    } catch (error) {
      console.error("Failed to add diver:", error);
    }
  };

  return (
    <div className="add-diver-container">
      <h2>Add New Diver to Group {groupId}</h2>
      <form onSubmit={handleSubmit} className="diver-form">
        {Object.keys(formData).map((key) => (
          key !== "status" ? (
            <input
              key={key}
              type="text"
              name={key}
              placeholder={key.replace("_", " ")}
              value={formData[key]}
              onChange={handleChange}
              required
            />
          ) : null
        ))}
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
