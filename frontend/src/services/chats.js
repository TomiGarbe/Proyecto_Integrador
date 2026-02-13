import api from './api';

export const getChat = (id_obra) => api.get(`/chat/${id_obra}`);
export const sendMessage = (id_obra, message) => {
  return api.post(`/chat/message/${id_obra}`, message, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
};