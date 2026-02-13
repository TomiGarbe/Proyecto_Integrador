import { useState, useEffect, useRef, useContext } from 'react';
import { useNavigate } from "react-router-dom"
import { AuthContext } from '../context/AuthContext';
import { useAuthRoles } from "../hooks/useAuthRoles";
import { getMantenimientosCorrectivos } from "../services/mantenimientoCorrectivoService";
import { getMantenimientosPreventivos } from "../services/mantenimientoPreventivoService";
import { get_notificaciones, notificacion_leida, delete_notificacion } from '../services/notificaciones';
import { subscribeToNotifications } from '../services/notificationWs';

const useNotifications = () => {
  const { logOut } = useContext(AuthContext);
  const { uid } = useAuthRoles()
  const [notifications, setNotifications] = useState([]);
  const [unreadCount, setUnreadCount] = useState(0);
  const socketRef = useRef(null);
  const navigate = useNavigate()
  const [showNotifications, setShowNotifications] = useState(false)

  const handleShowNotifications = () => setShowNotifications(true)
  const handleCloseNotifications = () => setShowNotifications(false)

  const fetchNotifications = async () => {
    try {
      if (!uid) return;

      const [correctivosResp, preventivosResp, notificacionesResp] = await Promise.all([
        getMantenimientosCorrectivos(uid),
        getMantenimientosPreventivos(uid),
        get_notificaciones(uid)
      ]);

      const correctivosMap = new Map(
        (correctivosResp.data || []).map(c => [Number(c.id_obra), Number(c.id)])
      );

      const preventivosMap = new Map(
        (preventivosResp.data || []).map(p => [Number(p.id_obra), Number(p.id)])
      );

      const notificaciones = Array.isArray(notificacionesResp.data)
      ? notificacionesResp.data
      : [];

      const mappedNotificaciones = notificaciones
        .map(notif => {
          const obraId = Number(notif.id_obra);

          if (correctivosMap.has(obraId)) {
            return {
              ...notif,
              tipo: "correctivo",
              id_mantenimiento: correctivosMap.get(obraId)
            };
          }

          if (preventivosMap.has(obraId)) {
            return {
              ...notif,
              tipo: "preventivo",
              id_mantenimiento: preventivosMap.get(obraId)
            };
          }

          return null;
        })
        .filter(Boolean);

      setUnreadCount(mappedNotificaciones.filter(n => !n.leida).length);
      mappedNotificaciones.sort(
        (a, b) => new Date(b.created_at) - new Date(a.created_at)
      );
      setNotifications(mappedNotificaciones);
    } catch (error) {
      console.error('Error obteniendo notificaciones:', error);
    }
  };

  useEffect(() => {
    if (uid) fetchNotifications();
  }, [uid]);

  useEffect(() => {
    if (!uid) return;

    const OPEN = typeof WebSocket !== 'undefined' ? WebSocket.OPEN : 1;
    if (socketRef.current && socketRef.current.readyState === OPEN) return;

    const onMessage = (data) => {
      setNotifications((prev) => {
        const updated = [data, ...prev];
        setUnreadCount(updated.filter((n) => !n.leida).length);
        return updated;
      });
    };

    const socket = subscribeToNotifications(uid, onMessage);
    socketRef.current = socket;

    return () => {
      const OPEN = typeof WebSocket !== 'undefined' ? WebSocket.OPEN : 1;
      if (socketRef.current?.close) {
        if (socketRef.current.readyState === OPEN) {
          socketRef.current.close();
        }
      } else if (socketRef.current?.disconnect) {
        socketRef.current.disconnect();
      }
      socketRef.current = null;
    };
  }, [uid]);

  const disconnect = () => {
    if (socketRef.current?.close) socketRef.current.close();
    else if (socketRef.current?.disconnect) socketRef.current.disconnect();
    socketRef.current = null;
  };

  const handleLogout = async () => {
    try {
      disconnect?.()
      await logOut()
    } catch (error) {
      console.error("Error al cerrar sesión:", error)
    }
  }

  const timeAgo = (timestamp) => {
    const now = new Date()
    const past = new Date(timestamp)
    const diff = Math.floor((now - past) / 1000)

    if (diff < 60) return `hace ${diff} seg`
    if (diff < 3600) return `hace ${Math.floor(diff / 60)} min`
    if (diff < 86400) return `hace ${Math.floor(diff / 3600)} h`

    const days = Math.floor(diff / 86400)
    const hours = Math.floor((diff % 86400) / 3600)
    const minutes = Math.floor((diff % 3600) / 60)
    const seconds = diff % 60

    let result = "hace "
    if (days > 0) result += `${days} d `
    if (hours > 0) result += `${hours} h `
    if (minutes > 0) result += `${minutes} min `
    if (seconds > 0) result += `${seconds} seg`
    return result.trim()
  }

  const handleClick = async (notification) => {
    if (notification.tipo === "correctivo") {
      const mantenimientoId = notification.id_mantenimiento
      navigate("/correctivo", { state: { mantenimientoId } })
    } else if (notification.tipo === "preventivo") {
      const mantenimientoId = notification.id_mantenimiento
      navigate("/preventivo", { state: { mantenimientoId } })
    }
    handleCloseNotifications()
    await notificacion_leida(notification.id)
    await fetchNotifications()
  }

  const handleDeleteNotification = async (notificationId, e) => {
    e.stopPropagation()
    try {
      await delete_notificacion(notificationId)
      await fetchNotifications()
    } catch (error) {
      console.error("Error al eliminar notificación:", error)
    }
  }

  const handleMarkAllAsRead = async () => {
    try {
      const notificacionesNoLeidas = notifications.filter((n) => !n.leida)

      await Promise.all(notificacionesNoLeidas.map((n) => notificacion_leida(n.id)))

      await fetchNotifications()
    } catch (error) {
      console.error("Error al marcar todas como leídas:", error)
    }
  }

  const handleDeleteReadNotifications = async () => {
    try {
      const leidas = notifications.filter((n) => n.leida)
      await Promise.all(leidas.map((n) => delete_notificacion(n.id)))
      await fetchNotifications()
    } catch (error) {
      console.error("Error al eliminar notificaciones leídas:", error)
    }
  }

  return { 
    notifications, 
    unreadCount, 
    showNotifications, 
    handleShowNotifications, 
    handleCloseNotifications, 
    handleLogout, 
    timeAgo, 
    handleClick, 
    handleDeleteNotification, 
    handleMarkAllAsRead, 
    handleDeleteReadNotifications
  };
};

export default useNotifications;