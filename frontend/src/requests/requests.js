import Cookies from "js-cookie";
import {toast} from "react-toastify";

const timezone = Intl.DateTimeFormat().resolvedOptions().timeZone;

export const local_frontend_url = 'http://localhost:3000'

export async function google_login(access_token) {
    return await fetch(`${local_frontend_url}/api/auth/google/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': Cookies.get('csrftoken'),
        },
        body: JSON.stringify({
            'token': access_token
        })
    })
        .then(res => res.json())
        .then(res => {
            if (res.access_token) {
                localStorage.setItem('token', res.access_token);
                window.location.replace(`${local_frontend_url}/profile`);
            } else {
                toast.warning("Cannot log in with provided credentials!");
            }
        });
}

export async function google_logout() {
    await fetch(`${local_frontend_url}/api/auth/google/logout/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            'token': localStorage.getItem("token"),
        })
    })
        .then(res => res.json())
        .then(data => {
            localStorage.clear();
            window.location.replace(`${local_frontend_url}/`);
        });
}

export async function getCurrentUser(token) {
    let user = {}
    await fetch(`${local_frontend_url}/api/auth/user/`, {
        headers: {
            "Content-Type": "application/json",
            'Authorization': `Bearer ${token}`,
            'Access-Control-Allow-Origin': 'http://localhost:3000',
            'X-CSRFToken': Cookies.get('csrftoken'),
            'Client-Location': timezone
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

export async function updateCurrentUser(user) {
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
            'Authorization': `Bearer ${localStorage.getItem("token")}`,
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
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem("token")}`,
            'Access-Control-Allow-Origin': 'http://localhost:3000',
            'X-CSRFToken': Cookies.get('csrftoken'),
            'Client-Location': timezone
        },
        credentials: 'include'
    })
        .then(res => res.json())
}

export async function getStudentClassesList() {
    return fetch(`${local_frontend_url}/api/english/student/classes/`, {
        headers: {
            "Content-Type": "application/json",
            'Authorization': `Bearer ${localStorage.getItem("token")}`,
            'Access-Control-Allow-Origin': 'http://localhost:3000',
            'X-CSRFToken': Cookies.get('csrftoken'),
            'Client-Location': timezone
        },
        credentials: 'include'
    })
        .then(res => res.json())
}

export async function getTeacherClassesList() {
    return fetch(`${local_frontend_url}/api/english/teacher/classes/`, {
        headers: {
            "Content-Type": "application/json",
            'Authorization': `Bearer ${localStorage.getItem("token")}`,
            'Access-Control-Allow-Origin': 'http://localhost:3000',
            'X-CSRFToken': Cookies.get('csrftoken'),
            'Client-Location': timezone
        },
        credentials: 'include'
    })
        .then(res => res.json())
}

export async function getStudentLessonsList() {
    return fetch(`${local_frontend_url}/api/english/student/lessons/`, {
        headers: {
            "Content-Type": "application/json",
            'Authorization': `Bearer ${localStorage.getItem("token")}`,
            'Access-Control-Allow-Origin': 'http://localhost:3000',
            'X-CSRFToken': Cookies.get('csrftoken'),
            'Client-Location': timezone
        },
        credentials: 'include'
    })
        .then(res => res.json())
}

export async function getTeacherLessonsList() {
    return fetch(`${local_frontend_url}/api/english/teacher/lessons/`, {
        headers: {
            "Content-Type": "application/json",
            'Authorization': `Bearer ${localStorage.getItem("token")}`,
            'Access-Control-Allow-Origin': 'http://localhost:3000',
            'X-CSRFToken': Cookies.get('csrftoken'),
            'Client-Location': timezone
        },
        credentials: 'include'
    })
        .then(res => res.json())
}

export async function getLessonByID(id) {
    return fetch(`${local_frontend_url}/api/english/teacher/lessons/${id}`, {
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem("token")}`,
            'Access-Control-Allow-Origin': 'http://localhost:3000',
            'X-CSRFToken': Cookies.get('csrftoken'),
            'Client-Location': timezone
        },
        credentials: 'include'
    })
        .then(res => res.json())
}

export async function cancelLessonByID(id) {
    const data = {status: "CANCELED"};
    await fetch(`${local_frontend_url}/api/english/teacher/lessons/${id}/`, {
        method: 'PATCH',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem("token")}`,
            'Access-Control-Allow-Origin': 'http://localhost:3000',
            'X-CSRFToken': Cookies.get('csrftoken'),
        },
        body: JSON.stringify(data),
    })
        .then(res => {
            if (res.ok) {
                window.location.replace(`${local_frontend_url}/english/lessons`);
            } else {
                toast.error(res.statusText);
            }
        });
}

export async function getClassByID(id) {
    return fetch(`${local_frontend_url}/api/english/teacher/classes/${id}`, {
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem("token")}`,
            'Access-Control-Allow-Origin': 'http://localhost:3000',
            'X-CSRFToken': Cookies.get('csrftoken'),
            'Client-Location': timezone
        },
        credentials: 'include'
    })
        .then(res => res.json())
}
