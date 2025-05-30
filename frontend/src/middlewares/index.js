import axios from "axios";




const instance = axios.create({
    // Use the environment variable for the backend server URL
    baseURL: process.env.VUE_APP_SERVER,
    headers: {
        'Content-Type': 'application/json; charset = utf-8'
    }
})

export default instance