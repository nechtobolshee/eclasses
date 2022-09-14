import React, {useState} from 'react';
import Header from "../components/Header";
import {register} from "../requests/requests";


const RegisterPage = () => {
    const [username, setUsername] = useState('');
    const [email, setEmail] = useState('');
    const [password1, setPassword1] = useState('');
    const [password2, setPassword2] = useState('');

    const onSubmit = async e => {
        e.preventDefault();
        const userData = {
            username: username,
            email: email,
            password1: password1,
            password2: password2
        };
        await register(userData)
    };

    return (
        <div>
            <header>
                <Header/>
            </header>
            <section className="vh-100">
                <div className="mask d-flex align-items-center h-100 gradient-custom-3">
                    <div className="container h-100">
                        <div className="row d-flex justify-content-center align-items-center h-100">
                            <div className="col-12 col-md-9 col-lg-7 col-xl-6">
                                <div className="main-raised">
                                    <div className="card-body p-5">
                                        <h2 className="text-uppercase text-center mb-5">Create an account</h2>
                                        <form onSubmit={onSubmit}>
                                            <div className="form-outline mb-4">
                                                <input name='username' type="username" required
                                                       onChange={e => setUsername(e.target.value)}
                                                       className="form-control form-control-lg" placeholder="Username"/>
                                            </div>

                                            <div className="form-outline mb-4">
                                                <input name='email' type="email" required
                                                       onChange={e => setEmail(e.target.value)}
                                                       className="form-control form-control-lg" placeholder="E-mail"/>
                                            </div>

                                            <div className="form-outline mb-4">
                                                <input name='password1' type="password" required
                                                       onChange={e => setPassword1(e.target.value)}
                                                       className="form-control form-control-lg" placeholder="Password"/>
                                            </div>

                                            <div className="form-outline mb-4">
                                                <input name='password2' type="password" required
                                                       onChange={e => setPassword2(e.target.value)}
                                                       className="form-control form-control-lg"
                                                       placeholder="Confirm password"/>
                                            </div>

                                            <div className="d-flex justify-content-center">
                                                <button type="submit" className="btn btn-dark btn-lg btn-block">Signup
                                                </button>
                                            </div>

                                            <p className="text-center text-muted mt-4 mb-1">Have already an
                                                account? <a href="/login/" className="fw-bold text-body"><u>Login
                                                    here</u></a>
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

export default RegisterPage;
