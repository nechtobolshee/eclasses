import React, {useEffect, useState} from "react";
import Header from "../components/Header";
import {getCurrentUser, getClassByID, local_frontend_url} from "../requests/requests";


const ClassPage = () => {
    const [class_name, setClassname] = useState("");
    const [students] = useState([]);
    const [teacher, setTeacher] = useState("");
    const [days, setDays] = useState("");
    const [start_time, setStartTime] = useState("");
    const [end_time, setEndTime] = useState("");
    const [id, setId] = useState("");

    useEffect(() => {
        const token = localStorage.getItem("token");
        if (token == null) {
            window.location.replace(`http://localhost:3000/login`);
        } else {
            const fetchData = async () => {
                const userData = await getCurrentUser(token);
                if (userData.role !== "Teacher") {
                    window.location.replace(`${local_frontend_url}/english/`);
                } else {
                    let route = window.location.href;
                    setId(route.split("/").pop());
                }
            }
            fetchData().catch(console.error);
        }
    }, []);

    useEffect(() => {
        const fetchData = async () => {
            const data = await getClassByID(id);
            setClassname(data.name);
            data.students.map((item) => (students.push(`${item.first_name} ${item.last_name}`)));
            setTeacher(`${data.teacher.first_name} ${data.teacher.last_name}`);
            setDays(data.days.join(", "));
            setStartTime(data.start_time);
            setEndTime(data.end_time);
        }
        fetchData().catch(console.error)
    }, [id]);

    return (
        <div>
            <header>
                <Header/>
            </header>
            <div className="main main-raised">
                <div className="container">
                    <div className="margin-content">
                        <h3 className="center-horizontal">Class details</h3>
                    </div>
                    <table className="table table-hover text-nowrap">
                        <tbody>
                        <tr>
                            <th scope="row">Class name</th>
                            <td>{class_name}</td>
                        </tr>
                        <tr>
                            <th scope="row">Days</th>
                            <td>{days}</td>
                        </tr>
                        <tr>
                            <th scope="row">Time start</th>
                            <td>{start_time}</td>
                        </tr>
                        <tr>
                            <th scope="row">Time end</th>
                            <td>{end_time}</td>
                        </tr>
                        <tr>
                            <th scope="row">Teacher</th>
                            <td>{teacher}</td>
                        </tr>
                        <tr>
                            <th scope="row">Students</th>
                            <td>{students.join(", ")}</td>
                        </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    )
};

export default ClassPage;
