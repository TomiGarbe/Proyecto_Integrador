import api from './api';

export const getSucursalesLocations = () => api.get('/maps/sucursales-locations');
export const getUsersLocations = () => api.get('/maps/users-locations');
export const getSelection = (id) => api.get(`/maps/selection/${id}`);
export const updateUserLocation = (location) => api.post('/maps/update-user-location', location);
export const selectObra = (seleccion) => api.post('/maps/select-obra', seleccion);
export const deleteSucursal = (id) => api.delete(`/maps/sucursal/${id}`);
export const deleteObra = (id) => api.delete(`/maps/delete-obra/${id}`);
export const deleteSelection = () => api.delete('/maps/selection');