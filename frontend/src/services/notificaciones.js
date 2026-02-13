import api from './api';

export const saveSubscription = (sub) => api.post('/push/subscribe', sub);
export const deleteSubscription = (endpoint) => api.delete('/push/unsubscribe', endpoint);
export const get_notificaciones = (firebase_uid) => api.get(`/notificaciones/${firebase_uid}`);
export const notificacion_leida = (id) => api.put(`/notificaciones/${id}`);
export const delete_notificaciones = (firebase_uid) => api.delete(`/notificaciones/${firebase_uid}`);
export const notify_nearby_maintenances = (payload) => api.post('/notificaciones/nearby', payload);
export const delete_notificacion = (id) => api.delete(`/notificaciones/delete/${id}`);