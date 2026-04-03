/**
 * Показывает всплывающее уведомление (toast)
 * @param {string} message - Текст сообщения
 * @param {string} type - Тип уведомления: 'success', 'error', 'info'
 */
export function showToast(message, type = "success") {
    const toast = document.createElement("div");
    
    // Базовые стили
    toast.style.position = "fixed";
    toast.style.bottom = "20px";
    toast.style.right = "20px";
    toast.style.padding = "12px 24px";
    toast.style.borderRadius = "8px";
    toast.style.color = "#fff";
    toast.style.fontWeight = "500";
    toast.style.boxShadow = "0 4px 12px rgba(0,0,0,0.15)";
    toast.style.zIndex = "1000";
    toast.style.transition = "opacity 0.3s, transform 0.3s";
    toast.style.opacity = "0";
    toast.style.transform = "translateY(20px)";
    toast.textContent = message;

    // Цвета в зависимости от типа
    if (type === "success") toast.style.backgroundColor = "#10b981"; // Зеленый
    else if (type === "error") toast.style.backgroundColor = "#ef4444"; // Красный
    else if (type === "info") toast.style.backgroundColor = "#3b82f6"; // Синий
    else toast.style.backgroundColor = "#6b7280"; // Серый

    document.body.appendChild(toast);

    // Анимация появления
    requestAnimationFrame(() => {
        toast.style.opacity = "1";
        toast.style.transform = "translateY(0)";
    });

    // Удаление через 3 секунды
    setTimeout(() => {
        toast.style.opacity = "0";
        toast.style.transform = "translateY(20px)";
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}
