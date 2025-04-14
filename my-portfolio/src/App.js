import React, { useRef, useState } from 'react';
import { FaGithub, FaInstagram, FaLinkedin} from 'react-icons/fa';
import Profile from './Profile';
import ProjectModal from './ProjectModal';

function App() {
  // Create refs for sections to scroll to
  const projectsRef = useRef(null);
  const contactRef = useRef(null);

  // Scroll to Projects section when "View My Work" is clicked
  const handleViewMyWork = () => {
    projectsRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  // Scroll to Contact section when "Contact Me" is clicked
  const handleContactMe = () => {
    contactRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  // Modal state for project details
  const [showModal, setShowModal] = useState(false);
  const [selectedProject, setSelectedProject] = useState(null);

  // Open modal when a project is clicked
  const handleProjectClick = (project) => {
    setSelectedProject(project);
    setShowModal(true);
  };

  // Close modal
  const handleCloseModal = () => {
    setShowModal(false);
    setSelectedProject(null);
  };

  // Sample data for your projects with additional details
  const projects = [
    {
      title: 'Clark',
      description: 'Clark is an advanced voice-activated AI assistant that blends natural conversation with real productivity tools. Designed to function as a personalized digital aide, Clark can manage emails, check calendars, synthesize speech, and handle daily tasks — all through seamless voice interaction.',
      image: '/clark.jpg',
      details: `Clark is an end-to-end intelligent voice assistant built using React, Flask, and OpenAI's GPT-4. It integrates with Google Calendar and Gmail APIs to manage emails and schedule events through natural language commands. Powered by Google's Text-to-Speech, Clark also provides real-time audio responses. The assistant supports wake word detection ("Hey Clark") and transitions into voice command mode, allowing users to interact hands-free. The project showcases expertise in full-stack development, natural language processing, voice UX, and third-party API integrations.`,
      links: [
        { label: 'GitHub', url: 'https://github.com/ucey-star/clark' },
        { label: 'Live Demo', url: 'https://drive.google.com/file/d/1ogM36E6G0Wy1xMyeycyps2FVG9VeRrZx/view?usp=sharing' }
      ]
    },
    {
      title: 'Object Detection for Cyclists',
      description: 'An intelligent real-time AI safety system engineered to support and protect cyclists by continuously monitoring their surroundings using computer vision. The system detects nearby objects such as vehicles and pedestrians, tracks their motion over time, and evaluates potential collision threats based on speed, distance, and positioning. By combining advanced object detection and multi-object tracking with spatial awareness, this project empowers cyclists with an extra layer of situational awareness — functioning like a virtual co-pilot that helps mitigate risk in dynamic urban environments.',
      image: '/odc.jpg',
      details: `This project combines object detection, multi-object tracking, and risk assessment to enhance situational awareness for cyclists. Built with Python and OpenCV, the system leverages the YOLOv8 model for real-time detection and DeepSORT for tracking multiple objects persistently across video frames. The application identifies common road objects (like cars and pedestrians), estimates their distance and speed using the pinhole camera model, and determines whether they're within a cyclist's immediate lane of travel. When a fast-moving object gets too close, the system issues an audible alert using a text-to-speech engine—creating a virtual safety co-pilot for urban cyclists.`,
      links: [
        { label: 'GitHub', url: 'https://github.com/ucey-star/AI-labs/tree/main/Cyclist_hazard_detector' },
      ]
    },    
    {
      title: 'The 8-Puzzle',
      description: 'This project is an AI-driven solution to the classic 8-puzzle problem. The goal of the assignment was to implement an optimal solver using the A* search algorithm in Python. The 8-puzzle is a sliding tile game where eight numbered tiles and one empty space are arranged in a 3×3 grid. The challenge is to reach a predefined goal configuration by sliding tiles into the empty space, one move at a time.',
      image: '/8puzzle.jpg',
      details: 'This project is an AI-driven solution to the classic 8-puzzle problem, which challenges you to arrange eight numbered tiles in a 3×3 grid into a specific goal configuration by sliding tiles into an empty space. In this project, I developed a robust A\* search-based solver using Python that efficiently finds the optimal sequence of moves by combining a custom-designed `PuzzleNode` class, multiple heuristic functions, and performance optimizations such as memoization. The `PuzzleNode` class encapsulates each state of the puzzle, tracking the current configuration, depth, evaluation value, and pointers to parent nodes to reconstruct the solution path. Two main heuristic functions were implemented—Misplaced Tiles and Manhattan Distance—to guide the search process, and an advanced heuristic extension was explored to further enhance efficiency by reducing unnecessary node expansions. The implementation also incorporates thorough error handling for invalid or unsolvable puzzles, ensuring that the algorithm gracefully terminates with appropriate error codes when necessary. Through extensive testing and validation, this project demonstrates not only the practical application of A\* search but also the importance of balancing algorithmic complexity with computational efficiency in solving challenging AI problems.',
      links: [
        { label: 'GitHb', url: 'https://github.com/ucey-star/AI-labs/tree/main/8-puzzle/index' },
      ]
    },
    {
      title: 'Expert system design (Prolog)',
      description: " I collaborated with Andriy Kashyrskyy and Trinh Nguyễn to design an expert system using Prolog and Python. Our project addresses the challenge that many students in Taipei face—finding reliable, accessible local recommendations for shopping, cultural learning, and relaxation. With the language barrier and scattered travel information complicating the search for worthwhile destinations, we built an AI-driven expert system that guides users through a series of tailored questions. This interactive approach helps narrow down options and delivers personalized recommendations based on the user's location, interests, and preferences, ensuring that the suggestions are both dependable and user-friendly.",
      image: 'esd.jpg',
      details: "In this project, I focused on developing and integrating the core components of our expert system. I contributed to the Prolog knowledge base, which stores detailed information about various locations in Taipei, and I helped build the Python interface that processes user inputs and queries the knowledge base. The system begins by confirming that the user is in Taipei, then asks about their primary intention—whether they want to shop, learn, or relax. Based on the user's responses, the system dynamically filters through a curated list of locations, taking into account attributes such as price range, entrance fees, ambiance, and setting. I also implemented several extensions, including a menu-based interface that improves input accuracy by correcting typos and mapping ambiguous responses to the correct options. Rigorous testing ensured that the system not only meets the project requirements but also delivers an intuitive and efficient experience for users exploring Taipei.",
      links: [
        { label: 'GitHb', url: 'https://github.com/ucey-star/AI-labs/tree/main/expert-system' },
        { label: 'Notebook', url: 'https://github.com/ucey-star/AI-labs/blob/main/expert-system/CS152%20LBA%20-%20Trinh%2C%20Uche%2C%20Andriy%202/CS152%20LBA%20-%20Jupyter%20Notebook%20-%20Trinh%2C%20Uche%2C%20Andriy.ipynb' }
      ]
    },
    {
      title: 'Tictactoe Minimax agent',
      description: "  I developed an AI agent to assess the performance of a Minimax AI in a 4x4 Tic Tac Toe game. The goal was to create a robust AI player capable of competing against both a computer-generated random opponent and a human player. By leveraging the minimax algorithm enhanced with alpha-beta pruning and iterative deepening, I tackled the challenge of efficiently exploring the game state space to determine the optimal moves. This project not only highlights my ability to implement advanced AI techniques but also demonstrates my commitment to evaluating and refining AI performance in competitive game scenarios.",
      image: 'tictactoe.jpg',
      details: "In this project, I implemented a dedicated class called TicTacToe_Minimax_Agent that integrates the minimax algorithm with critical enhancements such as alpha-beta pruning and iterative deepening, which significantly improved the search efficiency and decision-making process. I designed a heuristic evaluation function to score game states based on potential winning lines, guiding the AI to prioritize moves that increase its chances of winning. I rigorously tested the agent by simulating 100 games against a random opponent, which allowed me to measure its win rate and overall performance. Additionally, I developed functions to render the Tic Tac Toe board and accept human inputs, enabling interactive gameplay against the AI. I also extended the project by integrating a Tkinter-based GUI to create a more engaging user experience. Through this work, I gained valuable insights into algorithm optimization, heuristic design, and practical AI application in game development.",
      links: [
        { label: 'GitHb', url: 'https://github.com/ucey-star/OneBank' },
        { label: 'Live Demo', url: 'https://yourdemo.com' }
      ]
    },
    {
      title: 'One Bank',
      description: "One Bank is an AI-powered platform that helps users maximize credit card rewards by automatically recommending the best card to use for any given transaction. Users can securely upload their cards and preferred reward types. Then, using One Bank’s browser extension and backend intelligence, the system analyzes merchant data and transaction amounts in real time and suggests the optimal card based on reward potential—whether that’s cashback, miles, or points.",
      image: '/onebank.jpg',
      details: "The project includes a full-stack system built with Flask and React, backed by an AI recommendation engine that takes into account real-time context like merchant category and transaction amount. I implemented a rewards optimization algorithm that evaluates each card's benefits, including quarterly categories, custom reward structures, and socialized benefits added by the user. The browser extension integrates seamlessly into checkout pages and communicates with the backend to retrieve the best card for the situation. Beyond the extension, I developed APIs for card management, benefit editing, and transaction analysis, ensuring a robust and scalable platform. This project showcases my skills in AI logic, user interface design, backend development, and real-world deployment strategies.",
      links: [
        { label: 'GitHub', url: 'https://github.com/YourRepo' },
        { label: 'Live Demo', url: 'https://yourdemo.com' }
      ]
    },    
    {
      title: 'AI stock price prediction',
      description: "  I developed an AI agent to assess the performance of a Minimax AI in a 4x4 Tic Tac Toe game. The goal was to create a robust AI player capable of competing against both a computer-generated random opponent and a human player. By leveraging the minimax algorithm enhanced with alpha-beta pruning and iterative deepening, I tackled the challenge of efficiently exploring the game state space to determine the optimal moves. This project not only highlights my ability to implement advanced AI techniques but also demonstrates my commitment to evaluating and refining AI performance in competitive game scenarios.",
      image: 'tictactoe.jpg',
      details: "In this project, I implemented a dedicated class called TicTacToe_Minimax_Agent that integrates the minimax algorithm with critical enhancements such as alpha-beta pruning and iterative deepening, which significantly improved the search efficiency and decision-making process. I designed a heuristic evaluation function to score game states based on potential winning lines, guiding the AI to prioritize moves that increase its chances of winning. I rigorously tested the agent by simulating 100 games against a random opponent, which allowed me to measure its win rate and overall performance. Additionally, I developed functions to render the Tic Tac Toe board and accept human inputs, enabling interactive gameplay against the AI. I also extended the project by integrating a Tkinter-based GUI to create a more engaging user experience. Through this work, I gained valuable insights into algorithm optimization, heuristic design, and practical AI application in game development.",
      links: [
        { label: 'GitHb', url: 'https://github.com/YourRepo' },
        { label: 'Live Demo', url: 'https://yourdemo.com' }
      ]
    },
  ];

  return (
    <>
      {/*
        Global CSS in a <style> tag—everything is contained in one file.
      */}
      <style>{`
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;500;700&display=swap');

        * {
          margin: 0;
          padding: 0;
          box-sizing: border-box;
          font-family: 'Poppins', sans-serif;
        }

        body {
          background: linear-gradient(135deg, #b24592, #f15f79);
          color: #fff;
          overflow-x: hidden;
        }

        /* Hero Section */
        .hero {
          height: 100vh;
          display: flex;
          flex-direction: column;
          align-items: center;
          justify-content: center;
          text-align: center;
          padding: 2rem;
          background-attachment: fixed;
          background-size: cover;
        }

        .hero h1 {
          font-size: 4rem;
          font-weight: 700;
          letter-spacing: 2px;
          animation: fadeInDown 1.5s ease both;
          background: -webkit-linear-gradient(#fff, #eee);
          -webkit-background-clip: text;
          -webkit-text-fill-color: transparent;
        }

        .hero p {
          font-size: 1.2rem;
          margin: 1rem 0 2rem;
          max-width: 700px;
          animation: fadeInUp 1.5s ease both;
        }

        .hero button {
          font-size: 1rem;
          padding: 0.8rem 2rem;
          margin: 0.2rem;
          border: none;
          border-radius: 50px;
          background: #fff;
          color: #b24592;
          cursor: pointer;
          font-weight: 600;
          letter-spacing: 1px;
          box-shadow: 0 5px 15px rgba(0,0,0,0.3);
          transition: transform 0.3s ease, box-shadow 0.3s ease;
        }

        .hero button:hover {
          transform: scale(1.05);
          box-shadow: 0 8px 20px rgba(0,0,0,0.3);
        }

        /* Keyframe Animations */
        @keyframes fadeInDown {
          0% {
            opacity: 0;
            transform: translateY(-20px);
          }
          100% {
            opacity: 1;
            transform: translateY(0);
          }
        }

        @keyframes fadeInUp {
          0% {
            opacity: 0;
            transform: translateY(20px);
          }
          100% {
            opacity: 1;
            transform: translateY(0);
          }
        }

        /* Profile Section */
        .profile {
          display: flex;
          flex-direction: column;
          align-items: center;
          padding: 3rem 2rem;
          background: #fff;
          color: #333;
        }

        .profile-card {
          display: flex;
          align-items: center;
          max-width: 800px;
          background: #f5f5f5;
          padding: 2rem;
          border-radius: 10px;
          box-shadow: 0 5px 20px rgba(0,0,0,0.1);
        }

        .profile-image {
          width: 150px;
          height: 150px;
          border-radius: 50%;
          object-fit: cover;
          margin-right: 2rem;
        }

        .profile-info h2 {
          font-size: 2rem;
          margin-bottom: 0.5rem;
          color: #b24592;
        }

        .profile-info p {
          font-size: 1rem;
          line-height: 1.5;
        }

        /* Projects Section */
        .projects {
          min-height: 80vh;
          padding: 4rem 2rem;
          text-align: center;
          background: #fff;
          color: #333;
          position: relative;
          overflow: hidden;
        }

        /* Make the "My Projects" text gradient */
        .projects h2 {
          font-size: 3rem;
          margin-bottom: 2rem;
          background: linear-gradient(to right, #b24592, #f15f79);
          -webkit-background-clip: text;
          -webkit-text-fill-color: transparent;
        }

        .projects h2::after {
          content: "";
          width: 80px;
          height: 3px;
          background: linear-gradient(to right, #b24592, #f15f79);
          display: block;
          margin: 1rem auto 0;
        }

        /* Projects Grid */
        .projects-grid {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
          gap: 2rem;
          margin-top: 2rem;
        }

        /* Project Card */
        .project-card {
          background: #fff;
          border-radius: 10px;
          border: 1px solid #eee;
          box-shadow: 0 5px 20px rgba(0,0,0,0.1);
          overflow: hidden;
          transition: transform 0.3s ease, box-shadow 0.3s ease;
          cursor: pointer;
          position: relative;
        }

        /* Gradient overlay on hover */
        .project-card::before {
          content: "";
          position: absolute;
          top: 0; 
          left: 0;
          width: 100%; 
          height: 100%;
          border-radius: 10px;
          background: linear-gradient(135deg, #b24592, #f15f79);
          opacity: 0;
          transition: opacity 0.3s ease;
          z-index: 1;
          pointer-events: none;
        }

        .project-card:hover::before {
          opacity: 0.2;
        }

        .project-card:hover {
          transform: translateY(-5px);
          box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }

        .project-card img {
          width: 100%;
          height: 200px;
          object-fit: cover;
          transition: transform 0.3s ease;
        }

        .project-card:hover img {
          transform: scale(1.05);
        }

        .project-content {
          position: relative;
          padding: 1.2rem 1.5rem;
          z-index: 2; /* Above the overlay */
          transition: transform 0.3s ease;
        }

        .project-content h3 {
          margin-bottom: 0.5rem;
          font-size: 1.3rem;
        }

        .project-content p {
          font-size: 0.95rem;
          line-height: 1.4;
          color: #555;
        }

        /* About Section */
        .about {
          display: flex;
          flex-direction: column;
          align-items: center;
          justify-content: center;
          text-align: center;
          padding: 4rem 2rem;
          background: linear-gradient(135deg, #f15f79, #b24592);
        }

        .about h2 {
          font-size: 2.5rem;
          margin-bottom: 2rem;
        }

        .about p {
          max-width: 800px;
          font-size: 1rem;
          line-height: 1.7;
        }

        /* Contact Section */
        .contact {
          display: flex;
          flex-direction: column;
          align-items: center;
          text-align: center;
          padding: 4rem 2rem;
          background: #fff;
          color: #333;
        }

        .contact h2 {
          font-size: 2.5rem;
          margin-bottom: 1rem;
        }

        .social-icons {
          display: flex;
          gap: 1.5rem;
          margin-top: 2rem;
        }

        .icon-circle {
          background: #b24592;
          color: #fff;
          padding: 0.7rem;
          border-radius: 50%;
          transition: transform 0.3s ease;
          cursor: pointer;
        }

        .icon-circle:hover {
          transform: scale(1.2);
        }

        /* Footer */
        .footer {
          text-align: center;
          padding: 1rem;
          background: #222;
          color: #ccc;
          font-size: 0.9rem;
        }

        /* Modal Styles */
        .modal-overlay {
          position: fixed;
          top: 0;
          left: 0;
          width: 100%;
          height: 100%;
          background: rgba(0,0,0,0.7);
          display: flex;
          align-items: center;
          justify-content: center;
          z-index: 1000;
        }

        .modal-content {
          background: #fff;
          color: #333;
          padding: 2rem;
          border-radius: 10px;
          max-width: 600px;
          width: 90%;
          position: relative;
          animation: fadeIn 0.5s ease;
        }

        .modal-content img {
          width: 100%;
          height: auto;
          border-radius: 10px;
          margin-bottom: 1rem;
        }

        .modal-close {
          position: absolute;
          top: 10px;
          right: 10px;
          background: transparent;
          border: none;
          font-size: 1.5rem;
          cursor: pointer;
          color: #333;
        }

        @keyframes fadeIn {
          from { opacity: 0; transform: scale(0.9); }
          to { opacity: 1; transform: scale(1); }
        }

        /* Responsive */
        @media (max-width: 768px) {
          .hero h1 {
            font-size: 2.5rem;
          }

          .projects h2 {
            font-size: 2rem;
          }

          .about h2 {
            font-size: 2rem;
          }

          .contact h2 {
            font-size: 2rem;
          }

          .profile-card {
            flex-direction: column;
          }
          .profile-image {
            margin-right: 0;
            margin-bottom: 1rem;
          }
        }
      `}</style>

      {/* Hero Section */}
      <section className="hero">
        <h1>Welcome to My Portfolio</h1>
        <p>
          I harness the power of artificial intelligence to drive innovation and craft transformative solutions that blend cutting-edge algorithms with creative vision.
        </p>
        <button onClick={handleViewMyWork}>View My Work</button>
        <button onClick={handleContactMe}>Contact Me</button>
      </section>

      <Profile /> 

      {/* Projects Section */}
      <section className="projects" ref={projectsRef}>
        <h2>My Projects</h2>
        <div className="projects-grid">
          {projects.map((proj, idx) => (
            <div className="project-card" key={idx} onClick={() => handleProjectClick(proj)}>
              <img src={proj.image} alt={proj.title} />
              <div className="project-content">
                <h3>{proj.title}</h3>
                <p>{proj.description}</p>
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* About Section */}
      <section className="about">
        <h2>About Me</h2>
        <p>
          I’m a passionate developer and designer who loves pushing boundaries.
          With a keen eye for aesthetics and a focus on performance, I blend
          artistry with cutting-edge tech to deliver exceptional results.
          Whether it's building interactive UIs or crafting memorable brand
          identities, I always strive for excellence and innovation.
        </p>
      </section>

      {/* Contact Section */}
      <section className="contact" ref={contactRef}>
        <h2>Contact Me</h2>
        <p>Have a project in mind or want to collaborate? Let’s connect!</p>
        <div className="social-icons">
          <div className="icon-circle">
            <a href="https://github.com/ucey-star/"><FaGithub size={24} /></a>
          </div>
          <div className="icon-circle">
          <a href="https://www.linkedin.com/in/uchechukwu-unanka-b50088225/"><FaLinkedin size={24} /></a>
          </div>
          <div className="icon-circle">
          <a href="https://www.instagram.com/only.ucey?igsh=NTc4MTIwNjQ2YQ%3D%3D&utm_source=qr"><FaInstagram size={24} /></a> 
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="footer">
        © {new Date().getFullYear()} Uchechukwu Unanka - All Rights Reserved
      </footer>

      {/* Modal for Project Details */}
      {showModal && selectedProject && (
         <ProjectModal project={selectedProject} onClose={handleCloseModal} />
      )}
    </>
  );
}

export default App;
