import api from './api';

export const getMantenimientosCorrectivos = async () => {
  const response = await api.get('/mantenimientos-correctivos/');
  return {
    ...response,
    data: (response.data || []),
  };
};

export const getMantenimientoCorrectivo = async (id) => {
  const response = await api.get(`/mantenimientos-correctivos/${id}`);
  return {
    ...response,
    data: response.data,
  };
};

export const createMantenimientoCorrectivo = (mantenimiento) => {
  return api.post('/mantenimientos-correctivos/', mantenimiento);
};

export const updateMantenimientoCorrectivo = (id, mantenimiento) => {
  return api.put(`/mantenimientos-correctivos/${id}`, mantenimiento, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
};
export const deleteMantenimientoCorrectivo = (id) => api.delete(`/mantenimientos-correctivos/${id}`);
