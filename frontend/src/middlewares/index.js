import axios from "axios";



const instance = axios.create({
    baseURL: process.env.BACKEND_SERVER,
    headers: {
        'Content-Type': 'application/json; charset = utf-8'
    }
})

export default instance