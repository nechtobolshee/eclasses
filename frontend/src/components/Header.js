import React, { Component } from "react";
import {Link} from "react-router-dom";

class Header extends Component {
    render() {
        return (
            <div className="header">
                <div className="menu-area">
                    <nav className="main-menu">
                        <Link to="/english">Some picture</Link>
                        <Link className="nav-right" to={{pathname: "http://0.0.0.0:8000/docs/"}} target="_blank">Docs</Link>
                        <Link className="nav-right" to="/english/lessons">Lessons</Link>
                        <Link className="nav-right" to="/english">Classes</Link>
                        <Link className="nav-right" to="/profile">Profile</Link>
                    </nav>
                </div>
            </div>
        );
    }
}

export default Header;
