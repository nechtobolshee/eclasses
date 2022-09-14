import React, {useEffect, useState} from "react";
import Header from "../components/Header";
import {getCurrentUser, getStudentLessonsList, getTeacherLessonsList} from "../requests/requests";

const LessonsListPage = () => {
    const [userClassesList, setUserClassesList] = useState([]);

    useEffect(() => {
        const token = localStorage.getItem('token')
        if (token == null) {
            window.location.replace(`http://localhost:3000/login`);
        } else {
            const fetchData = async () => {
                const userData = await getCurrentUser(token)
                if (userData.role === "Teacher") {
                    setUserClassesList(await getTeacherLessonsList());
                } else {
                    setUserClassesList(await getStudentLessonsList());
                }
            }
            fetchData().catch(console.error)
        }
    }, []);

    return (
        <div>
            <header>
                <Header/>
            </header>
            <div className="main main-raised">
                <div className="container">
                    <div className="margin-content">
                        <h3 className="center-horizontal">Lessons</h3>
                    </div>
                    <table className="table table-hover text-nowrap">
                        <thead className="table-active">
                        <tr>
                            <th>Name</th>
                            <th>Status</th>
                            <th>Time start</th>
                            <th>Time end</th>
                        </tr>
                        </thead>
                        <tbody id="tableData">
                        {
                            userClassesList.map((item) => (
                                <tr key={item.pk}>
                                    <td>{item.class_name}</td>
                                    <td>{item.status}</td>
                                    <td>{item.start_time}</td>
                                    <td>{item.end_time}</td>
                                </tr>
                            ))
                        }
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    )
};

export default LessonsListPage;
