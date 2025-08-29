import React, { useState } from "react";
import axios from "axios";
import "./Help.css";

export default function Help() {
  const [form, setForm] = useState({ name: "", email: "", message: "" });
  const [sent, setSent] = useState(false);

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await axios.post("http://localhost:5000/contact", form);
      setSent(true);
    } catch (err) {
      alert("Failed to send message. Please try again later.");
    }
  };

  return (
    <div className="help-container">
      <h2>Contact Us</h2>
      {sent ? (
        <div className="success-message">Your message was sent successfully!</div>
      ) : (
        <form className="help-form" onSubmit={handleSubmit}>
          <input
            type="text"
            name="name"
            placeholder="Your Name"
            value={form.name}
            onChange={handleChange}
            required
          />
          <input
            type="email"
            name="email"
            placeholder="Your Email"
            value={form.email}
            onChange={handleChange}
            required
          />
          <textarea
            name="message"
            placeholder="Your Message"
            value={form.message}
            onChange={handleChange}
            required
            rows={5}
          />
          <button type="submit">Send</button>
        </form>
      )}
    </div>
  );
}
