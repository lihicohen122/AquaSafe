import React from "react";
import "./Help.css";

export default function Help() {
  return (
    <div className="help-container">
      <h2>Contact Us</h2>
      <div className="contact-info">
        <p>
          Have a question or suggestion? We'd love to hear from you!<br />
          Feel free to reach out to us directly:
        </p>
        
        <div className="email-section">
          <h3>📧 Email Us 📧</h3>
          <div className="email-addresses">
            <div className="email-item">
              <strong>Noa Halali:</strong> 
              <a href="mailto:noa4000@gmail.com">noa4000@gmail.com</a>
            </div>
            <div className="email-item">
              <strong>Lihi Cohen:</strong> 
              <a href="mailto:lihicohen122@gmail.com">lihicohen122@gmail.com</a>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
