import React from "react";
import Header from "../components/Header";

const UpdateProfilePage = () =>(
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
                                    <h2 className="text-uppercase text-center mb-5">Edit profile</h2>
                                    <form>
                                        <div className="form-outline mb-4">
                                            <input type="text" className="form-control form-control-lg" placeholder="Name"/>
                                        </div>

                                        <div className="form-outline mb-4">
                                            <input type="email" className="form-control form-control-lg" placeholder="Surname"/>
                                        </div>

                                        <div className="form-outline mb-4">
                                            <label className="form-label">Select new avatar</label>
                                            <input type="file" className="mb-4" id="customFile"/>
                                        </div>

                                        <div className="d-flex justify-content-center">
                                            <button type="button" className="btn btn-dark btn-lg btn-block">Update</button>
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
);

export default UpdateProfilePage;
