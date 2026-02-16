import api from './api';
import { getClientes } from './clienteService';

const normalizeSucursal = (sucursal, clienteNombre) => ({
  ...sucursal,
  cliente_nombre: clienteNombre ?? sucursal.cliente_nombre ?? '',
  frecuencia_preventivo: sucursal.frecuencia_preventivo ?? null,
});

export const getSucursales = async () => {
  const [clientesResp, sucursalesResp] = await Promise.all([
    getClientes(),
    api.get('/sucursales/')
  ]);

  const clientes = clientesResp.data || [];
  const sucursales = sucursalesResp.data || [];

  const clienteMap = new Map(clientes.map(c => [c.id, c.nombre]));

  return {
    data: sucursales.map(s =>
      normalizeSucursal(s, clienteMap.get(s.id_cliente))
    )
  };
};

export const getSucursalesByCliente = async (clienteId) => {
  const [clientesResp, sucursalesResp] = await Promise.all([
    getClientes(),
    api.get(`/sucursales/${clienteId}`)
  ]);
  const clientes = clientesResp.data || [];
  const sucursales = sucursalesResp.data || [];
  const clienteMap = new Map(clientes.map(c => [c.id, c.nombre]));

  return {
    data: sucursales.map(s =>
      normalizeSucursal(s, clienteMap.get(s.id_cliente))
    )
  };
};

export const getSucursal = (id) => api.get(`/sucursales/${id}`);

export const createSucursal = (clienteId, sucursal) =>
  api.post(`/sucursales/`, {
    ...sucursal,
    id_cliente: clienteId,
    frecuencia_preventivo: sucursal.frecuencia_preventivo || null,
  });

export const updateSucursal = (id, sucursal) =>
  api.put(`/sucursales/${id}`, {
    ...sucursal,
    frecuencia_preventivo: sucursal.frecuencia_preventivo || null,
  });

export const deleteSucursal = (id) => api.delete(`/sucursales/${id}`);
