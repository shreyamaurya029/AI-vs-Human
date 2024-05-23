// Contributors.jsx
import React, { useState, useEffect } from "react";
import { FaEnvelope } from "react-icons/fa"; // Import icons from react-icons library
import "./Contributors.scss";

const Contributors = () => {
  const [professors, setProfessors] = useState([]);
  const [students, setStudents] = useState([]);
  const [researchScholars, setResearchScholars] = useState([]);
  useEffect(() => {
    fetch("/db/contributors.json")
      .then((response) => {
        if (!response.ok) {
          throw new Error("Failed to fetch contributors");
        }
        return response.json();
      })
      .then((data) => {
        const profs = data.filter((contributor) => contributor.role === "Professor");
        const stus = data.filter((contributor) => contributor.role === "Student");
        const resScholars = data.filter(
          (contributor) => contributor.role === "Research Scholar"
        );
        setProfessors(profs);
        setStudents(stus);
        setResearchScholars(resScholars);
      })
      .catch((error) => console.error("Error fetching contributors:", error));
  }, []);

  // Contributors.jsx

  const renderContributors = (contributors) =>
    contributors.map((contributor) => (
      <div key={contributor.id} className="contributor-card">
        <img
          src={contributor.profilePic}
          alt={contributor.name}
          className="contributor-image"
        />
        <div className="contributor-details">
          <h2 className="contributor-name">{contributor.name}</h2>
          <p className="contributor-role">{contributor.role}</p>
          <div className="contact-icons">
            <div className="contact-info">
              <FaEnvelope className="email-icon" />
              <span>{contributor.email}</span>
            </div>
            {/* <div className="contact-info">
              <FaPhone className="phone-icon" />
              <span>{contributor.phone}</span>
            </div> */}
          </div>
        </div>
      </div>
    ));

  return (
    <div className="contributors">
      <div className="contributors-container">
        <div className="contributors-section">
          <h1 className="contributors-heading">Guides</h1>
          <div className="contributors">{renderContributors(professors)}</div>
        </div>
        <div className="contributors-section">
          <h1 className="contributors-heading">Research Scholars</h1>
          <div className="contributors">{renderContributors(researchScholars)}</div>
        </div>
        <div className="contributors-section">
          <h1 className="contributors-heading">Students</h1>
          <div className="contributors">{renderContributors(students)}</div>
        </div>
      </div>
    </div>
  );
};

export default Contributors;
