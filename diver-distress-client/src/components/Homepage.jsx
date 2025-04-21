import React from "react";
import { useNavigate } from "react-router-dom";
import "./Homepage.css"; // Import CSS for styling

const Homepage = () => {
  const navigate = useNavigate();

  // Mock data for groups (replace with actual data from your backend or state)
  const groups = [
    { id: 1, name: "Coral Divers" },
    { id: 2, name: "Deep Sea Explorers" },
    { id: 3, name: "Blue Ocean Team" },
  ];

  const handleGroupClick = (groupId) => {
    navigate(`/group/${groupId}`);
  };

  const handleAddGroup = () => {
    // Logic for adding a group (e.g., open a modal or navigate to a form)
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