import api from './api';

export const getMantenimientosPreventivos = async () => {
  const response = await api.get('/mantenimientos-preventivos/');
  return {
    ...response,
    data: (response.data || []),
  };
};

export const getMantenimientoPreventivo = async (id) => {
  const response = await api.get(`/mantenimientos-preventivos/${id}`);
  return {
    ...response,
    data: response.data,
  };
};

export const createMantenimientoPreventivo = (mantenimiento) => {
  return api.post('/mantenimientos-preventivos/', mantenimiento);
};

export const updateMantenimientoPreventivo = (id, mantenimiento) => {
  return api.put(`/mantenimientos-preventivos/${id}`, mantenimiento, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
};
export const deleteMantenimientoPreventivo = (id) => api.delete(`/mantenimientos-preventivos/${id}`);
