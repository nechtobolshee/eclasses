import React, {useEffect} from "react";
import Header from "../components/Header";
import {GoogleLogin} from 'react-google-login';
import {gapi} from 'gapi-script';
import {google_login} from "../requests/requests";


const LoginPage = () => {
    const clientId = require('../client_credentials.json').client_id;

    const onSuccess = async (res) => {
        await google_login(res.accessToken)
    };
    const onFailure = (error) => {
        console.log('Login failed.', error);
    };

    useEffect(() => {
        if (localStorage.getItem("token") !== null) {
            window.location.replace("http://localhost:3000/profile");
        }
        const initClient = () => {
            gapi.auth2.init({
                clientId: clientId,
                scope: ''
            });
        };
        gapi.load('client:auth2', initClient);
    });

    return (
        <div>
            <header>
                <Header/>
            </header>
            <section className="vh-100">
                <div className="container h-100">
                    <div className="row justify-content-center align-items-center h-100">
                        <div className="main-raised">
                            <div className="card-body p-5">
                                <h2 className="text-uppercase text-center mb-4">Sign into your account</h2>
                                <div className="d-flex justify-content-center">
                                    <GoogleLogin
                                        clientId={clientId}
                                        buttonText="Sign in with Google"
                                        onSuccess={onSuccess}
                                        onFailure={onFailure}
                                        cookiePolicy={'single_host_origin'}
                                        loginHint
                                    />
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </section>
        </div>
    );
}

export default LoginPage;
