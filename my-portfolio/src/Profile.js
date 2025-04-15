import React from 'react';

const Profile = () => (
  <>
    <style>{`
      .profile {
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 3rem 2rem;
        background: #fff;
        color: #333;
        /* Animate background color */
        animation: gradientMove 10s ease infinite;
      }

      @keyframes gradientMove {
        0% { background: #fff; }
        50% { background: #f0f0f0; }
        100% { background: #fff; }
      }

      .profile-card {
        display: flex;
        align-items: center;
        max-width: 800px;
        background: linear-gradient(135deg, #f5f5f5, #fff);
        padding: 2rem;
        border-radius: 10px;
        box-shadow: 0 5px 20px rgba(0, 0, 0, 0.1);
        /* Slide in effect */
        animation: slideIn 1s ease-out;
      }

      @keyframes slideIn {
        from { transform: translateY(50px); opacity: 0; }
        to { transform: translateY(0); opacity: 1; }
      }

      .profile-image {
        width: 150px;
        height: 150px;
        border-radius: 50%;
        object-fit: cover;
        margin-right: 2rem;
        border: 3px solid;
        /* Floating animation */
        animation: float 3s ease-in-out infinite;
      }

      @keyframes float {
        0% { transform: translateY(0); }
        50% { transform: translateY(-10px); }
        100% { transform: translateY(0); }
      }

      .profile-info h2 {
        font-size: 2rem;
        margin-bottom: 0.3rem;
        color: #b24592;
        /* Fade in text */
        animation: fadeIn 1.5s ease-out;
      }

      .profile-info h3 {
        font-size: 1.5rem;
        margin: 0.3rem 0;
        animation: fadeIn 2s ease-out;
      }

      .profile-info h4 {
        font-size: 1.2rem;
        margin: 0.3rem 0;
        font-style: italic;
        color: #555;
        animation: fadeIn 2.5s ease-out;
      }

      .profile-info p {
        font-size: 1rem;
        line-height: 1.5;
        margin-top: 1rem;
        animation: fadeIn 3s ease-out;
      }

      @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
      }

      @media (max-width: 768px) {
        .profile-card {
          flex-direction: column;
          text-align: center;
        }
        .profile-image {
          margin-right: 0;
          margin-bottom: 1rem;
        }
      }
    `}</style>
    <section className="profile">
      <div className="profile-card">
        <img 
          src="/profile.jpg" 
          alt="Uchechukwu Unanka" 
          className="profile-image" 
        />
        <div className="profile-info">
          <h2>Uchechukwu Unanka</h2>
          <h3>Minerva University</h3>
          <h4>Computational Sciences</h4>
          <p>
            I'm a software engineer with a strong foundation in computational sciences and a passion for building AI-driven solutions that blend creativity, data, and design. From intelligent voice assistants to real-time computer vision systems, I love crafting tools that make technology feel intuitive, useful, and human-centered.
          </p>
        </div>
      </div>
    </section>
  </>
);

export default Profile;
