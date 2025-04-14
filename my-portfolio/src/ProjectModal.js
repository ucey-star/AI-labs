import React from 'react';

const ProjectModal = ({ project, onClose }) => (
  <>
    <style>{`
      /* Overlay Styles */
      .modal-overlay {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: radial-gradient(circle at center, rgba(0,0,0,0.6), rgba(0,0,0,0.9));
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 9999;
        animation: fadeInOverlay 0.5s ease forwards;
      }
      @keyframes fadeInOverlay {
        from { opacity: 0; }
        to   { opacity: 1; }
      }

      /* Modal Container Styles */
      .modal-content {
        background: rgba(255, 255, 255, 0.90);
        backdrop-filter: blur(12px);
        color: #333;
        padding: 2.5rem;
        border-radius: 15px;
        max-width: 600px;
        width: 90%;
        max-height: 80vh;
        overflow-y: auto;
        position: relative;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
        animation: slideInUp 0.5s ease forwards;
      }
      @keyframes slideInUp {
        from {
          opacity: 0;
          transform: translateY(40px);
        }
        to {
          opacity: 1;
          transform: translateY(0);
        }
      }

      /* Heading with Gradient Text */
      .modal-content h2 {
        margin-bottom: 1rem;
        font-size: 2rem;
        background: linear-gradient(90deg, #b24592, #f15f79);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
      }

      /* Image Styling & Hover Zoom */
      .modal-content img {
        display: block;
        width: 100%;
        height: auto;
        max-height: 300px;
        object-fit: cover;
        border-radius: 10px;
        margin-bottom: 1.5rem;
        transition: transform 0.3s ease;
      }
      .modal-content img:hover {
        transform: scale(1.03);
      }

      /* Details Container for Project Description */
      .modal-details {
        background-color: #f9f9f9;
        border: 1px solid #eee;
        border-radius: 10px;
        padding: 1rem;
        margin-bottom: 1rem;
      }
      .modal-details p {
        margin: 0;
        font-size: 1rem;
        line-height: 1.6;
        color: #555;
      }

      /* Modal Links Styles */
      .modal-links {
        display: flex;
        flex-wrap: wrap;
        gap: 0.8rem;
        margin-top: 1rem;
      }
      .modal-links a {
        background: linear-gradient(90deg, #b24592, #f15f79);
        color: #fff;
        padding: 0.5rem 1rem;
        border-radius: 25px;
        text-decoration: none;
        font-size: 0.9rem;
        transition: opacity 0.3s ease, transform 0.3s ease;
      }
      .modal-links a:hover {
        opacity: 0.9;
        transform: scale(1.05);
      }

      /* Close Button */
      .modal-close {
        position: absolute;
        top: 15px;
        right: 15px;
        background: transparent;
        border: none;
        font-size: 2rem;
        cursor: pointer;
        color: #333;
        transition: color 0.3s ease, transform 0.3s ease;
      }
      .modal-close:hover {
        color: #b24592;
        transform: scale(1.2);
      }
    `}</style>

    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <button className="modal-close" onClick={onClose}>&times;</button>
        <h2>{project.title}</h2>
        <img src={project.image} alt={project.title} />
        <div className="modal-details">
          <p>{project.details}</p>
        </div>
        {project.links && project.links.length > 0 && (
          <div className="modal-links">
            {project.links.map((link, index) => (
              <a key={index} href={link.url} target="_blank" rel="noopener noreferrer">
                {link.label}
              </a>
            ))}
          </div>
        )}
      </div>
    </div>
  </>
);

export default ProjectModal;
