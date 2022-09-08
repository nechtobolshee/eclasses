import React from "react";
import Header from "../components/Header";

const HomePage = () =>(
    <div>
        <header>
            <Header />
        </header>
        <div className="main main-raised">
            <div className="container">
                <div className="center-horizontal">
                    <h2>Default Home page</h2>
                </div>
                <div className="p-5">
                    <a href="login/" className="btn btn-dark btn-lg btn-block">Signin</a>
                    <a href="register/" className="btn btn-dark btn-lg btn-block">Signup</a>
                </div>
            </div>
        </div>
    </div>
);

export default HomePage;
