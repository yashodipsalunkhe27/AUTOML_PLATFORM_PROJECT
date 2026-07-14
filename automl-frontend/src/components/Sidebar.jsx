import { NavLink } from "react-router-dom";
import "../styles/sidebar.css";

import {
  FaChartPie,
  FaCloudUploadAlt,
  FaSearchengin,
  FaCogs,
  FaMagic,
  FaLayerGroup,
  FaTrophy,
  FaFileAlt,
  FaHistory,
  FaSlidersH,
  FaRobot,
  FaUserCircle,
} from "react-icons/fa";

function Sidebar({ collapsed, mobileOpen }) {

  const sidebarClass = [
    "sidebar",
    collapsed ? "collapsed" : "",
    mobileOpen ? "mobile-open" : "",
  ]
    .filter(Boolean)
    .join(" ");

  return (
    <div className={sidebarClass}>

      <div className="sidebar-logo">
        <FaRobot className="logo-icon" />
        <h2>AutoML</h2>
      </div>

      <nav>

        <div className="nav-section-label">Workspace</div>

        <NavLink to="/" end className="nav-link">
          <FaChartPie className="nav-icon" />
          <span>Dashboard</span>
        </NavLink>

        <NavLink to="/upload" className="nav-link">
          <FaCloudUploadAlt className="nav-icon" />
          <span>Upload</span>
        </NavLink>

        <NavLink to="/analysis" className="nav-link">
          <FaSearchengin className="nav-icon" />
          <span>Analysis</span>
        </NavLink>

        <NavLink to="/train" className="nav-link">
          <FaCogs className="nav-icon" />
          <span>Train</span>
        </NavLink>

        <NavLink to="/prediction" className="nav-link">
          <FaMagic className="nav-icon" />
          <span>Prediction</span>
        </NavLink>

        <NavLink to="/batch" className="nav-link">
          <FaLayerGroup className="nav-icon" />
          <span>Batch Prediction</span>
        </NavLink>

        <div className="nav-section-label">Insights</div>

        <NavLink to="/results" className="nav-link">
          <FaTrophy className="nav-icon" />
          <span>Results</span>
        </NavLink>

        <NavLink to="/reports" className="nav-link">
          <FaFileAlt className="nav-icon" />
          <span>Reports</span>
        </NavLink>

        <NavLink to="/history" className="nav-link">
          <FaHistory className="nav-icon" />
          <span>History</span>
        </NavLink>

        <div className="nav-section-label">Preferences</div>

        <NavLink to="/settings" className="nav-link">
          <FaSlidersH className="nav-icon" />
          <span>Settings</span>
        </NavLink>

      </nav>

      <div className="sidebar-footer">
        <FaUserCircle className="footer-avatar" />
        <div className="footer-text">
          <div className="footer-name">User</div>
          <div className="footer-role">AutoML Member</div>
        </div>
      </div>

    </div>
  );
}

export default Sidebar;