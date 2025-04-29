import api from './api';

export const getSucursales = () => api.get('/sucursales/');
export const getSucursal = (id) => api.get(`/sucursales/${id}`);
export const createSucursal = (sucursal) => api.post('/sucursales/', sucursal);
export const updateSucursal = (id, sucursal) => api.put(`/sucursales/${id}`, sucursal);
export const deleteSucursal = (id) => api.delete(`/sucursales/${id}`);