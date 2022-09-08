import React, { Component } from "react";
import {Link} from "react-router-dom";

class Header extends Component {
    render() {
        return (
            <div className="header">
                <div className="menu-area">
                    <nav className="main-menu">
                        <Link to="/">Some picture</Link>
                        <Link class="nav-right" to="#">FAQ</Link>
                        <Link class="nav-right" to="#">Lessons</Link>
                        <Link class="nav-right" to="#">Classes</Link>
                        <Link class="nav-right" to="/profile">Profile</Link>
                        <Link class="nav-right" to="/">Home</Link>
                    </nav>
                </div>
            </div>
        );
    }
}

export default Header;