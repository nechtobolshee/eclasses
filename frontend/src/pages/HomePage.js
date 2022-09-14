import React, {useState, useEffect} from "react";
import Header from "../components/Header";
import {logout, getCurrentUser, local_frontend_url} from "../requests/requests";

const HomePage = () => {
    const [authorized, setAuthorized] = useState(false);
    const [first_name, setFirstname] = useState('');

    useEffect(() => {
        const token = localStorage.getItem('token')
        if (token !== null) {
            const fetchData = async () => {
                const data = await getCurrentUser(token)
                setFirstname(data.first_name);
                setAuthorized(true);
            }
            fetchData().catch(console.error)
        }
    }, [authorized]);

    async function toLogout() {
        await logout(localStorage.getItem('token'))
        window.location.replace(`${local_frontend_url}/`)
    }

    return (
        <div>
            <header>
                <Header/>
            </header>
            <div className="main main-raised">
                <div className="container">
                    <div className="center-horizontal">
                        <h2>
                            {authorized &&
                                <div>Hello{first_name && `, ${first_name}`}!</div>
                            }
                            {!authorized &&
                                <div>Log in to continue</div>
                            }
                        </h2>
                    </div>
                    <div className="p-5">
                        {authorized &&
                            <button className="btn btn-dark btn-lg btn-block" onClick={toLogout}>Logout</button>
                        }
                        {!authorized &&
                            <div>
                                <a href="login/" className="btn btn-dark btn-lg btn-block">Login</a>
                                <a href="register/" className="btn btn-dark btn-lg btn-block">Register</a>
                            </div>
                        }
                    </div>
                </div>
            </div>
        </div>
    )
};

export default HomePage;
