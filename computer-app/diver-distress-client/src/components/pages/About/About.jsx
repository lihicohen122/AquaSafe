import React from "react";
import "./About.css";
import aboutImage from "../../../images/team-photo.jpg";

export default function About() {
  return (
    <div className="about-container">
      <h2>About Us</h2>
      <p>
        We are two computer science students who love diving and enjoying life!<br />
        AquaSafe was created as part of our academic project to help divers stay safe using smart technology.
      </p>
      <p>
        Feel free to contact us for any question or suggestion!
      </p>
      <div className="about-names">
        <strong>Noa Halali</strong><br />
        <strong>Lihi Cohen</strong>
      </div>
      <div className="about-image">
        <img src={aboutImage} alt="About Us" />
      </div>
    </div>
  );
}
