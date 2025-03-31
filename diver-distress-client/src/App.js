import React, { useState, useEffect } from "react";
import axios from "axios";

function App() {
  const [message, setMessage] = useState("");
  const [status, setStatus] = useState("");

  // Fetch the message from the / endpoint
  useEffect(() => {
    axios
      .get("http://localhost:5000/")
      .then((response) => setMessage(response.data.message))
      .catch((error) => console.error("Error fetching message:", error));
  }, []);

  // Fetch the status from the /status endpoint
  useEffect(() => {
    axios
      .get("http://localhost:5000/status")
      .then((response) => setStatus(response.data.status))
      .catch((error) => console.error("Error fetching status:", error));
  }, []);

  return (
    <div>
      <h1>Diver Distress System</h1>
      <p>{message}</p>
      <p>Status: {status}</p>
    </div>
  );
}

export default App;
