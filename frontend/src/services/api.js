import axios from 'axios';
import { API_URL } from '../config'; 
 
 const api = axios.create({
    baseURL: API_URL, // Usamos la variable obtenida de config.js
 });
 
 export default api;