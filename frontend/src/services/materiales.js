import api from './api';

export const getMateriales = () => api.get('/materiales/');
export const getMaterial = (id) => api.get(`/materiales/${id}`);
export const getMovimientos = () => api.get('/materiales/movimientos/');
export const getMovimiento = (id) => api.get(`/materiales/movimientos/${id}`);
export const createMaterial = (material) => api.post('/materiales/', material);
export const registrarMovimiento = (movimiento) => api.post('/materiales/movimientos/', movimiento);
export const updateMaterial = (id, material) => api.put(`/materiales/${id}`, material);
export const updateMovimiento = (id, movimiento) => api.put(`/materiales/movimientos/${id}`, movimiento);