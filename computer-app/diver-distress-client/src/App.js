import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import SensorDashboard from "./components/pages/Homepage/Groups/Dashboard/SensorDashboard";
import Homepage from "./components/pages/Homepage/Homepage";
import DiverDetails from "./components/pages/Homepage/Groups/Dashboard/Divers/DiverDetails";
import NavigationBar from "./components/layout/NavigationBar";
import AddDiver from "./components/pages/Homepage/Groups/Dashboard/Divers/AddDiver";
import DeleteDiver from "./components/pages/Homepage/Groups/Dashboard/Divers/DeleteDiver";
import Help from "./components/pages/Help/Help";
import About from "./components/pages/About/About";
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
            <Route path="/help" element={<Help />} />
            <Route path="/about" element={<About />} />
          </Routes>
        </div>
      </div>
    </Router>
  );
}

export default App;