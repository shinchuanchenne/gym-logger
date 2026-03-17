const API_BASE_URL = "http://127.0.0.1:8000";

function saveToken(token){
    localStorage.setItem("token", token);
}

function getToken(){
    return localStorage.getItem("token");
}

function clearToken(){
    localStorage.removeItem("token");
}