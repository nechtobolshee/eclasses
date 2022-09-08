import React from "react";
import Header from "../components/Header";

const ProfilePage = () =>(
    <div>
        <header>
            <Header />
        </header>
        <div className="main main-raised">
            <div className="container">
                <div className="center-horizontal margin-content">
                    <img src="https://cutt.ly/DCQslAH" alt="Circle" className="img-raised rounded-circle img-fluid"></img>
                </div>
                <div className="margin-content">
                    <h3 className="center-horizontal">Metthew Betcher</h3>
                </div>
                <table class="table table-hover text-nowrap">
                    <tbody>
                        <tr className="table-active">
                            <th scope="row" colspan="2">Information</th>
                        </tr>
                        <tr>
                            <th scope="row">First Name</th>
                            <td>Metthew</td>
                        </tr>
                        <tr>
                            <th scope="row">Last Name</th>
                            <td>Bettcher</td>
                        </tr>
                        <tr>
                            <th scope="row">E-mail</th>
                            <td>mail@gmail.com</td>
                        </tr>
                    </tbody>
                </table>
                <div className="d-flex justify-content-center">
                    <a href="profile/edit/" className="btn btn-dark btn-lg btn-block">Edit</a>
                </div>
            </div>
        </div>
    </div>
);

export default ProfilePage;