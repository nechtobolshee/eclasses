import Cookies from "js-cookie";
import {toast} from "react-toastify";

export const local_frontend_url = 'http://localhost:3000'

export async function login(user) {
    await fetch(`${local_frontend_url}/api/auth/login/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': 'http://localhost:3000',
            'X-CSRFToken': Cookies.get('csrftoken'),
        },
        body: JSON.stringify(user),
        credentials: "include"
    })
        .then(res => res.json())
        .then(data => {
            if (data.key) {
                localStorage.setItem('token', data.key);
                window.location.replace(`${local_frontend_url}/profile`);
            } else {
                toast.warning("Cannot log in with provided credentials!");
            }
        });
}

export async function logout(token) {
    await fetch(`${local_frontend_url}/api/auth/logout/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            Authorization: `Token ${token}`
        },
        credentials: "include"
    })
        .then(res => res.json())
        .then(data => {
            localStorage.clear();
            window.location.replace(`${local_frontend_url}/`);
        });
}

export async function register(user) {
    await fetch(`${local_frontend_url}/api/auth/registration/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': 'http://localhost:3000',
            'X-CSRFToken': Cookies.get('csrftoken'),
        },
        body: JSON.stringify(user),
    })
        .then(res => {
            if (res.ok) {
                window.location.replace(`${local_frontend_url}/profile`);
            } else {
                toast.error(res.statusText);
            }
        });
}

export async function getCurrentUser(token) {
    let user = {}
    await fetch(`${local_frontend_url}/api/auth/user/`, {
        headers: {
            "Content-Type": "application/json",
            'Authorization': `Token ${token}`,
            'Access-Control-Allow-Origin': 'http://localhost:3000',
            'X-CSRFToken': Cookies.get('csrftoken')
        },
        credentials: 'include'
    })
        .then(res => res.json())
        .then((result) => {
            if (result.hasOwnProperty('detail')) {
                localStorage.clear();
                window.location.replace(`${local_frontend_url}/login`);
            } else {
                user = result
            }
        })
    return user
}

export async function updateCurrentUser(token, user) {
    const formData = new FormData();
    if (user.avatar) {
        formData.append('avatar', user.avatar)
    }
    if (user.first_name) {
        formData.append('first_name', user.first_name)
    }
    if (user.last_name) {
        formData.append('last_name', user.last_name)
    }

    await fetch(`${local_frontend_url}/api/auth/user/`, {
        method: 'PATCH',
        headers: {
            'Access-Control-Allow-Origin': 'http://localhost:3000',
            'X-CSRFToken': Cookies.get('csrftoken')
        },
        body: formData

    })
        .then(res => {
            if (res.ok) {
                window.location.replace(`${local_frontend_url}/profile`);
            } else {
                toast.error(res.statusText);
            }
        });
}

export async function getClassesList() {
    return fetch(`${local_frontend_url}/api/english/`, {
        headers: {
            "Content-Type": "application/json",
            'Access-Control-Allow-Origin': 'http://localhost:3000',
            'X-CSRFToken': Cookies.get('csrftoken')
        },
        credentials: 'include'
    })
        .then(res => res.json())
}

export async function getStudentClassesList() {
    return fetch(`${local_frontend_url}/api/english/student/classes/`, {
        headers: {
            "Content-Type": "application/json",
            'Access-Control-Allow-Origin': 'http://localhost:3000',
            'X-CSRFToken': Cookies.get('csrftoken')
        },
        credentials: 'include'
    })
        .then(res => res.json())
}

export async function getTeacherClassesList() {
    return fetch(`${local_frontend_url}/api/english/teacher/classes/`, {
        headers: {
            "Content-Type": "application/json",
            'Access-Control-Allow-Origin': 'http://localhost:3000',
            'X-CSRFToken': Cookies.get('csrftoken')
        },
        credentials: 'include'
    })
        .then(res => res.json())
}

export async function getStudentLessonsList() {
    return fetch(`${local_frontend_url}/api/english/student/lessons/`, {
        headers: {
            "Content-Type": "application/json",
            'Access-Control-Allow-Origin': 'http://localhost:3000',
            'X-CSRFToken': Cookies.get('csrftoken')
        },
        credentials: 'include'
    })
        .then(res => res.json())
}

export async function getTeacherLessonsList() {
    return fetch(`${local_frontend_url}/api/english/teacher/lessons/`, {
        headers: {
            "Content-Type": "application/json",
            'Access-Control-Allow-Origin': 'http://localhost:3000',
            'X-CSRFToken': Cookies.get('csrftoken')
        },
        credentials: 'include'
    })
        .then(res => res.json())
}