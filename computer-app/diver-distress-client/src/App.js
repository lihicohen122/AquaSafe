import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import SensorDashboard from "./components/SensorDashboard";
import Homepage from "./components/Homepage";
import DiverDetails from "./components/DiverDetails";
import NavigationBar from "./components/NavigationBar";
import AddDiver from "./components/AddDiver";
import DeleteDiver from "./components/DeleteDiver";
import "./App.css";

function App() {
  return (
    <Router>
      <div className="App">
        <NavigationBar />
        <div className="content">
          <Routes>
            <Route path="/" element={<Homepage />} />
            <Route path="/group/:groupId" element={<SensorDashboard />} />
            <Route path="/diver/:diverId" element={<DiverDetails />} />
            <Route path="/add-diver/:groupId" element={<AddDiver />} />
            <Route path="/delete-diver/:groupId" element={<DeleteDiver />} />
          </Routes>
        </div>
      </div>
    </Router>
  );
}

export default App;