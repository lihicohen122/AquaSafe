import React, { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import axios from "axios";
import "./DeleteDiver.css";

export default function DeleteDiver() {
  const { groupId } = useParams();
  const [divers, setDivers] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    axios.get(`http://localhost:5000/groups/${groupId}`)
      .then(response => setDivers(response.data.divers))
      .catch(error => console.error("Failed to fetch divers:", error));
  }, [groupId]);

  const handleDelete = async (diverId) => {
    try {
      await axios.delete(`http://localhost:5000/divers/${diverId}`);
      setDivers(prev => prev.filter(diver => diver.id !== diverId));
    } catch (error) {
      console.error("Failed to delete diver:", error);
    }
  };

  return (
    <div className="delete-diver-container">
      <h2>Delete Divers from Group {groupId}</h2>
      <ul className="diver-list">
        {divers.map(diver => (
          <li key={diver.id} className="diver-item">
            <span>{diver.name} (ID: {diver.id})</span>
            <button onClick={() => handleDelete(diver.id)}>Delete</button>
          </li>
        ))}
      </ul>
      <button onClick={() => navigate(`/group/${groupId}`)}>Back to Group</button>
    </div>
  );
}
