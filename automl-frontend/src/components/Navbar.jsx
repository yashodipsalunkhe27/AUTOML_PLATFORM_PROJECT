import "../styles/navbar.css";

function Navbar() {
  return (
    <header className="navbar">
      <div className="navbar-title">
        <h2>AutoML Platform</h2>
      </div>

      <div className="navbar-right">
        <span>Welcome, User 👋</span>
      </div>
    </header>
  );
}

export default Navbar;