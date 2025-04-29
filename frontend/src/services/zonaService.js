import api from './api';

export const getZonas = () => api.get('/zonas/');
export const createZona = (zona) => api.post('/zonas/', zona);
export const deleteZona = (id) => api.delete(`/zonas/${id}`);