import React, { useState } from "react";
import axios from "axios";
import "./AddGroup.css";

export default function AddGroup({ onGroupAdded, onCancel }) {
  const [formData, setFormData] = useState({
    name: ""
  });
  const [error, setError] = useState("");

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const validateForm = () => {
    if (!formData.name.trim()) {
      setError("Group name is required");
      return false;
    }
    return true;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!validateForm()) return;
    try {
      const response = await axios.post("http://localhost:5000/groups", formData);
      if (onGroupAdded) onGroupAdded(response.data);
      setFormData({ name: "" });
      setError("");
    } catch (err) {
        if (err.response && err.response.data && err.response.data.detail) {
            if (Array.isArray(err.response.data.detail)) {
                setError(err.response.data.detail.map(e => e.msg).join(', '));
            } else {
                setError(err.response.data.detail);
            }
        } else {
        setError("Failed to add group. Please try again.");
        }
}
  };

  return (
    <div className="add-group-container">
      <h2>Add New Group</h2>
      {error && <div className="error-message">{error}</div>}
      <form onSubmit={handleSubmit} className="group-form">
        <input
          type="text"
          name="name"
          placeholder="Group Name"
          value={formData.name}
          onChange={handleChange}
          required
        />
        <button type="submit">Add Group</button>
        <button type="button" onClick={onCancel}>Cancel</button>
      </form>
    </div>
  );
}
