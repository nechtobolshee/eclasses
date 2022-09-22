import React, {useEffect} from 'react';
import {GoogleLogin} from 'react-google-login';
import {gapi} from 'gapi-script';
import {google_login} from "../requests/requests";


const GoogleSocialAuth = () => {
    const clientId = require('../client_credentials.json').client_id;

    useEffect(() => {
        const initClient = () => {
            gapi.auth2.init({
                clientId: clientId,
                scope: ''
            });
        };
        gapi.load('client:auth2', initClient);
    });

    const onSuccess = async (res) => {
        await google_login(res.accessToken)
    };

    const onFailure = (error) => {
        console.log('Login failed.', error);
    };

    return (
        <GoogleLogin
            clientId={clientId}
            buttonText="Sign in with Google"
            onSuccess={onSuccess}
            onFailure={onFailure}
            cookiePolicy={'single_host_origin'}
            loginHint
        />
    );
}

export default GoogleSocialAuth;