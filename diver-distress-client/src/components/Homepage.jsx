import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import '../styles/GlobalStyles.css';
import "./Homepage.css";

const Homepage = () => {
  const navigate = useNavigate();
  const [groups, setGroups] = useState([]);

  useEffect(() => {
    axios.get("http://localhost:5000/groups")
      .then(response => setGroups(response.data))
      .catch(error => console.error("Error fetching groups:", error));
  }, []);

  const handleGroupClick = (groupId) => {
    navigate(`/group/${groupId}`);
  };

  const handleAddGroup = () => {
    alert("Add Group functionality to be implemented!");
  };

  return (
    <div className="homepage-container">
      <header className="homepage-header">
        <h1>Welcome to AquaSafe</h1>
        <p>Your ultimate diving companion</p>
      </header>
      <main>
        <h2>Your Diving Groups</h2>
        <ul className="group-list">
          {groups.map((group) => (
            <li
              key={group.id}
              className="group-item"
              onClick={() => handleGroupClick(group.id)}
            >
              {group.name}
            </li>
          ))}
        </ul>
        <button className="add-group-button" onClick={handleAddGroup}>
          + Add Group
        </button>
      </main>
    </div>
  );
};

export default Homepage;