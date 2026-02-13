import api from './api';

export const deletePlanilla = (id, fileName) => api.delete(`/obras/${id}/planilla/${fileName}`);
export const deleteFoto = (id, fileName) => api.delete(`/obras/${id}/fotos/${fileName}`);