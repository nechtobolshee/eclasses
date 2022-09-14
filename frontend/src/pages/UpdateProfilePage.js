import React, {useState} from "react";
import Header from "../components/Header";
import {updateCurrentUser} from "../requests/requests";

const UpdateProfilePage = () => {
    const [first_name, setFirstName] = useState(null);
    const [last_name, setLastName] = useState(null);
    const [avatar, setAvatar] = useState(null);

    const token = localStorage.getItem('token')
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
        await updateCurrentUser(token, userData)
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
                                        <h2 className="text-uppercase text-center mb-5">Edit profile</h2>
                                        <form onSubmit={onSubmit}>
                                            <div className="form-outline mb-4">
                                                <input type="text" className="form-control form-control-lg"
                                                       placeholder="Name" onChange={e => setFirstName(e.target.value)}/>
                                            </div>

                                            <div className="form-outline mb-4">
                                                <input type="text" className="form-control form-control-lg"
                                                       placeholder="Surname"
                                                       onChange={e => setLastName(e.target.value)}/>
                                            </div>

                                            <div className="form-outline mb-4">
                                                <label className="form-label">Select new avatar</label>
                                                <input type="file" accept="image/png, image/jpeg" className="mb-4"
                                                       onChange={e => setAvatar(e.target.files[0])}/>
                                            </div>

                                            <div className="d-flex justify-content-center">
                                                <button type="submit" className="btn btn-dark btn-lg btn-block">Update
                                                </button>
                                            </div>
                                        </form>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </section>
        </div>
    )
};

export default UpdateProfilePage;
