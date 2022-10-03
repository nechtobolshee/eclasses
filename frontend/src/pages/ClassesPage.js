import React, {useEffect, useState} from "react";
import Header from "../components/Header";
import {
    getClassesList,
    getCurrentUser,
    getStudentClassesList,
    getTeacherClassesList,
    leaveClass,
    joinClass
} from "../requests/requests";


const ClassesListPage = () => {
    const [user, setUser] = useState(null)
    const [classesList, setClassesList] = useState([]);
    const [userClassesList, setUserClassesList] = useState([]);
    const [joinButton, setJoinButton] = useState(false)


    useEffect(() => {
        const token = localStorage.getItem("token")
        if (token == null) {
            window.location.replace(`http://localhost:3000/login`);
        } else {
            const fetchData = async () => {
                const userData = await getCurrentUser(token)
                setUser(userData)
                setClassesList(await getClassesList());
                if (userData.role === "Teacher") {
                    setUserClassesList(await getTeacherClassesList());
                } else {
                    setUserClassesList(await getStudentClassesList());
                    setJoinButton(true)
                }
            }
            fetchData().catch(console.error)
        }
    }, []);

    const singleClass = (id) => () => {
        if (user?.role === "Teacher") {
            window.location.replace(`http://localhost:3000/english/classes/${id}`)
        }
    }

    const leaveClassFunc = (id) => async () => {
        await leaveClass(id)
    }

    const joinClassFunc = (id) => async () => {
        await joinClass(id)
    }

    return (
        <div>
            <header>
                <Header/>
            </header>
            <div className="main main-raised">
                <div className="container">
                    <div className="margin-content">
                        <h3 className="center-horizontal">My classes</h3>
                    </div>
                    <table className="table table-hover text-nowrap">
                        <thead className="table-active">
                        <tr>
                            <th>Name</th>
                            <th>Teacher</th>
                            <th>Days</th>
                            <th>Time start</th>
                            <th>Time end</th>
                            {joinButton === true &&
                                <th></th>
                            }
                        </tr>
                        </thead>
                        <tbody id="tableData">
                        {
                            userClassesList.map((item) => (
                                <tr key={item.pk} onClick={singleClass(item.pk)}>
                                    <td>{item.name}</td>
                                    <td>{item.teacher.first_name} {item.teacher.last_name}</td>
                                    <td>{item.days.join(", ")}</td>
                                    <td>{item.start_time}</td>
                                    <td>{item.end_time}</td>
                                    {joinButton === true &&
                                        <td><a href="/english/" className="pretty-link" onClick={leaveClassFunc(item.pk)}>Leave</a></td>
                                    }
                                </tr>
                            ))
                        }
                        </tbody>
                    </table>
                </div>
            </div>

            <div className="main main-raised">
                <div className="container">
                    <div className="margin-content">
                        <h3 className="center-horizontal">All classes</h3>
                    </div>
                    <table className="table table-hover text-nowrap">
                        <thead className="table-active">
                        <tr>
                            <th>Name</th>
                            <th>Teacher</th>
                            <th>Days</th>
                            <th>Time start</th>
                            <th>Time end</th>
                            {joinButton === true &&
                                <th></th>
                            }
                        </tr>
                        </thead>
                        <tbody id="tableData">
                        {
                            classesList.map((item) => (
                                <tr key={item.pk}>
                                    <td>{item.name}</td>
                                    <td>{item.teacher.first_name} {item.teacher.last_name}</td>
                                    <td>{item.days.join(", ")}</td>
                                    <td>{item.start_time}</td>
                                    <td>{item.end_time}</td>
                                    {joinButton === true &&
                                        <td><a href="/english/" className="pretty-link" onClick={joinClassFunc(item.pk)}>Join</a></td>
                                    }
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

export default ClassesListPage;
