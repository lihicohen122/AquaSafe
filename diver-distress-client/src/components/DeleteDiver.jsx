import React, { useEffect, useState, useCallback } from "react";
import { useNavigate, useParams } from "react-router-dom";
import axios from "axios";
import "./DeleteDiver.css";

export default function DeleteDiver() {
  const { groupId } = useParams();
  const [divers, setDivers] = useState([]);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);
  const navigate = useNavigate();

  const fetchDivers = useCallback(async () => {
    try {
      const response = await axios.get(`http://localhost:5000/groups/${groupId}`);
      // Sort divers: critical first, then warning, then others
      const sortedDivers = response.data.divers.sort((a, b) => {
        if (a.status === 'critical' && b.status !== 'critical') return -1;
        if (a.status !== 'critical' && b.status === 'critical') return 1;
        if (a.status === 'warning' && b.status !== 'warning') return -1;
        if (a.status !== 'warning' && b.status === 'warning') return 1;
        return 0;
      });
      setDivers(sortedDivers);
      setError(null);
    } catch (error) {
      setError("Failed to fetch divers. Please try again.");
      console.error("Failed to fetch divers:", error);
    }
  }, [groupId]);

  useEffect(() => {
    fetchDivers();
  }, [fetchDivers]);

  const handleDelete = async (diverId) => {
    try {
      await axios.delete(`http://localhost:5000/divers/${diverId}`);
      setSuccess(`Diver ${diverId} was successfully deleted`);
      await fetchDivers();
    } catch (error) {
      setError("Failed to delete diver. Please try again.");
      console.error("Failed to delete diver:", error);
    }
  };

  const getStatusClass = (status) => {
    switch (status) {
      case 'critical':
        return 'status-critical';
      case 'warning':
        return 'status-warning';
      default:
        return 'status-normal';
    }
  };

  return (
    <div className="delete-diver-container">
      <h2>Delete Divers from Group {groupId}</h2>
      {error && <div className="error-message">{error}</div>}
      {success && <div className="success-message">{success}</div>}
      <ul className="diver-list">
        {divers.map(diver => (
          <li key={diver.id} className={`diver-item ${getStatusClass(diver.status)}`}>
            <div className="diver-info">
              <span className="diver-name">{diver.name}</span>
              <span className="diver-id">(ID: {diver.id})</span>
              <span className="diver-status">{diver.status}</span>
            </div>
            <button 
              onClick={() => handleDelete(diver.id)}
              className="delete-button"
            >
              Delete
            </button>
          </li>
        ))}
      </ul>
      <button 
        onClick={() => navigate(`/group/${groupId}`)}
        className="back-button"
      >
        Back to Group
      </button>
    </div>
  );
}
