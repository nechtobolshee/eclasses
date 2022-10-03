import React, {useState} from "react";
import Header from "../components/Header";
import {updateCurrentUser} from "../requests/requests";


const UpdateProfilePage = () => {
    const [first_name, setFirstName] = useState(null);
    const [last_name, setLastName] = useState(null);
    const [avatar, setAvatar] = useState(null);

    const token = localStorage.getItem("token")
    if (token == null) {
        window.location.replace(`http://localhost:3000/login`);
    }

    const onSubmit = async e => {
        e.preventDefault();
        const userData = Object.assign({},
            first_name && {first_name: first_name},
            last_name && {last_name: last_name},
            avatar && {avatar: avatar}
        );
        await updateCurrentUser(userData)
    };

    return (
        <div>
            <header>
                <Header/>
            </header>

            <div className="center-horizontal">
                <div className="main main-raised default-small-block">
                    <div className="container">
                        <h2 className="text-uppercase text-center mb-5">Edit profile</h2>
                        <form onSubmit={onSubmit}>
                            <div>
                                <div className="form-outline mb-4">
                                    <input type="text" className="form-control form-control-lg"
                                           placeholder="Name" onChange={e => setFirstName(e.target.value)}/>
                                </div>

                                <div className="form-outline mb-4">
                                    <input type="text" className="form-control form-control-lg"
                                           placeholder="Surname"
                                           onChange={e => setLastName(e.target.value)}/>
                                </div>
                            </div>
                            <label className="form-label">Select new avatar</label>
                            <div className="form-outline mb-4">
                                <input type="file" accept="image/png, image/jpeg" className="mb-4"
                                       onChange={e => setAvatar(e.target.files[0])}/>
                            </div>
                            <div>
                                <button type="submit" className="btn btn-dark btn-lg btn-block">Update</button>
                                <a href="/profile/" className="btn btn-outline-dark btn-lg btn-block">Cancel</a>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    )
};

export default UpdateProfilePage;
