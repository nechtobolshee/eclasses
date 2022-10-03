import React, {useEffect, useState} from "react";
import Header from "../components/Header";
import default_avatar from "../images/default_avatar.jpg";
import {local_frontend_url, getCurrentUser, google_logout} from "../requests/requests";


const ProfilePage = () => {
    const [first_name, setFirstname] = useState("");
    const [last_name, setLastname] = useState("");
    const [username, setUsername] = useState("");
    const [email, setEmail] = useState("");
    const [role, setRole] = useState("");
    const [avatar, setAvatar] = useState(null);

    useEffect(() => {
        const token = localStorage.getItem("token");
        if (token == null) {
            window.location.replace(`${local_frontend_url}/login`);
        } else {
            const fetchData = async () => {
                const data = await getCurrentUser(token)
                setFirstname(data.first_name);
                setLastname(data.last_name);
                setUsername(data.username);
                setEmail(data.email);
                setRole(data.role);
                setAvatar(data.avatar);
            }
            fetchData().catch(console.error)
        }
    }, []);

    async function toLogout() {
        await google_logout()
        window.location.replace(`${local_frontend_url}/login`)
    }

    return (
        <div>
            <header>
                <Header/>
            </header>
            <div className="main main-raised">
                <div className="container">
                    <div className="center-horizontal margin-content">
                        {avatar &&
                            <img src={avatar} alt="Profile"
                                 className="avatar-size"></img>
                        }
                        {!avatar &&
                            <img src={default_avatar} alt="Circle"
                                 className="avatar-size"></img>
                        }
                    </div>
                    <div className="margin-content">
                        <h3 className="center-horizontal">{first_name} {last_name}</h3>
                    </div>
                    <table className="table table-hover text-nowrap">
                        <tbody>
                        <tr className="table-active">
                            <th scope="row" colSpan="2">Information</th>
                        </tr>
                        <tr>
                            <th scope="row">First Name</th>
                            <td>{first_name}</td>
                        </tr>
                        <tr>
                            <th scope="row">Last Name</th>
                            <td>{last_name}</td>
                        </tr>
                        <tr>
                            <th scope="row">Username</th>
                            <td>{username}</td>
                        </tr>
                        <tr>
                            <th scope="row">E-mail</th>
                            <td>{email}</td>
                        </tr>
                        <tr>
                            <th scope="row">Role</th>
                            <td>{role}</td>
                        </tr>
                        </tbody>
                    </table>
                    <div>
                        <a href="/profile/edit/" className="btn btn-dark btn-lg btn-block">Edit</a>
                        <button className="btn btn-outline-dark btn-lg btn-block" onClick={toLogout}>Logout</button>
                    </div>
                </div>
            </div>
        </div>
    )
};

export default ProfilePage;
