import React, {useEffect, useState} from "react";
import Header from "../components/Header";
import {getCurrentUser, getLessonByID, cancelLessonByID} from "../requests/requests";


const LessonPage = () => {
    const [class_name, setClassname] = useState("");
    const [status, setStatus] = useState("");
    const [start_time, setStartTime] = useState("");
    const [end_time, setEndTime] = useState("");
    const route = window.location.href;

    useEffect(() => {
        const token = localStorage.getItem("token");
        if (token == null) {
            window.location.replace(`http://localhost:3000/login`);
        } else {
            const fetchData = async () => {
                const userData = await getCurrentUser(token)
                if (userData.role !== "Teacher") {
                    window.location.replace(`http://localhost:3000/english/lessons`);
                }
            }
            fetchData().catch(console.error);
        }
    });

    useEffect(() => {
        const fetchData = async () => {
            const data = await getLessonByID(route.split("/").pop());
            setClassname(data.class_name);
            setStatus(data.status);
            setStartTime(data.start_time);
                setEndTime(data.end_time);
        }
        fetchData().catch(console.error)
    });

    async function cancelLesson() {
        await cancelLessonByID(route.split("/").pop())
    }

    return (
        <div>
            <header>
                <Header/>
            </header>
            <div className="main main-raised">
                <div className="container">
                    <div className="margin-content">
                        <h3 className="center-horizontal">Lesson details</h3>
                    </div>
                    <table className="table table-hover text-nowrap">
                        <tbody>
                        <tr>
                            <th scope="row">Class name</th>
                            <td>{class_name}</td>
                        </tr>
                        <tr>
                            <th scope="row">Status</th>
                            <td>{status}</td>
                        </tr>
                        <tr>
                            <th scope="row">Time start</th>
                            <td>{start_time}</td>
                        </tr>
                        <tr>
                            <th scope="row">Time end</th>
                            <td>{end_time}</td>
                        </tr>
                        </tbody>
                    </table>
                    <div className="">
                        <button className="btn btn-dark btn-lg btn-block" onClick={cancelLesson}>Cancel</button>
                        <a href="/english/lessons/" className="btn btn-outline-dark btn-lg btn-block">Back</a>
                    </div>
                </div>
            </div>
        </div>
    )
};

export default LessonPage;
