import React, { useState } from 'react';
import Header from "../components/Header";


const LoginPage = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const onSubmit = async e => {
        e.preventDefault();

        const updateUserData = {
          email: email,
          password: password
        };
    };

    return (
        <div>
            <header>
                <Header />
            </header>
            <section className="vh-100">
                <div className="mask d-flex align-items-center h-100 gradient-custom-3">
                    <div className="container h-100">
                        <div className="row d-flex justify-content-center align-items-center h-100">
                            <div className="col-12 col-md-9 col-lg-7 col-xl-6">
                                <div className="main-raised">
                                    <div className="card-body p-5">
                                        <h2 className="text-uppercase text-center mb-5">Sign into your account</h2>
                                        <form onSubmit={onSubmit}>
                                            <div className="form-outline mb-4">
                                                <input name="email" type="email" required onChange={e => setEmail(e.target.value)} className="form-control form-control-lg" placeholder="E-mail"/>
                                            </div>

                                            <div className="form-outline mb-4">
                                                <input name="password" type="password" required onChange={e => setPassword(e.target.value)} className="form-control form-control-lg" placeholder="Password"/>
                                            </div>

                                            <div className="d-flex justify-content-center">
                                                <button type='submit' className="btn btn-dark btn-lg btn-block">Login</button>
                                            </div>

                                            <p className="text-center text-muted mt-4 mb-0">
                                                Don't have an account? <a href="/register/" className="fw-bold text-body"><u>Register here</u></a>
                                            </p>
                                        </form>
                                    </div>
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
