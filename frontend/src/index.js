import React from 'react';
import {BrowserRouter, Route, Switch} from "react-router-dom";
import { ToastContainer } from 'react-toastify';
import ReactDOM from 'react-dom';

import './css/styles.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import 'react-toastify/dist/ReactToastify.css';

import ProfilePage from './pages/ProfilePage';
import UpdateProfilePage from "./pages/UpdateProfilePage";
import LoginPage from "./pages/LoginPage";
import RegisterPage from "./pages/RegisterPage";


ReactDOM.render(
    <BrowserRouter>
        <Switch>
            <Route exact path="/profile/" component={ProfilePage} />
            <Route exact path="/profile/edit/" component={UpdateProfilePage} />
            <Route exact path="/login/" component={LoginPage} />
            <Route exact path="/register/" component={RegisterPage} />
        </Switch>
        <ToastContainer
            position="top-right"
            autoClose={4000}
            hideProgressBar
            newestOnTop={false}
            closeOnClick
            rtl={false}
            pauseOnFocusLoss
            draggable
            pauseOnHover/>
    </BrowserRouter>,
  document.getElementById('root')
);