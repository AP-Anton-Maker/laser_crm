<?php
/**
 * FOHOW Landing Page - Обработчик формы (send.php)
 * Принимает POST-запрос, валидирует поля, отправляет письмо на email
 * 
 * ИНСТРУКЦИЯ ПО НАСТРОЙКЕ:
 * 1. Измените переменную $to на ваш email адрес
 * 2. При необходимости настройте SMTP или используйте стандартную mail() функцию
 * 3. Загрузите файл на хостинг
 */

// ============================================
// НАСТРОЙКИ
// ============================================

// EMAIL ДЛЯ РЕДАКТИРОВАНИЯ: Укажите ваш email для получения заявок
$to = 'info@fohow.ru'; // <-- ЗАМЕНИТЕ НА ВАШ EMAIL

// Тема письма
$subject = 'Новая заявка с сайта FOHOW';

// ============================================
// ПРОВЕРКА МЕТОДА ЗАПРОСА
// ============================================
if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    // Если не POST запрос - редирект на главную
    header('Location: index.php');
    exit;
}

// ============================================
// ПОЛУЧЕНИЕ И ОЧИСТКА ДАННЫХ
// ============================================

// Функция для очистки данных
function cleanInput($data) {
    return htmlspecialchars(trim($data), ENT_QUOTES, 'UTF-8');
}

// Получаем данные из формы
$name = isset($_POST['name']) ? cleanInput($_POST['name']) : '';
$phone = isset($_POST['phone']) ? cleanInput($_POST['phone']) : '';
$email = isset($_POST['email']) ? cleanInput($_POST['email']) : '';
$agreement = isset($_POST['agreement']) ? true : false;

// ============================================
// ВАЛИДАЦИЯ
// ============================================
$errors = [];

// Проверка имени (обязательное, минимум 2 символа)
if (empty($name)) {
    $errors[] = 'Имя обязательно для заполнения';
} elseif (strlen($name) < 2) {
    $errors[] = 'Имя должно содержать минимум 2 символа';
}

// Проверка телефона (обязательное)
if (empty($phone)) {
    $errors[] = 'Телефон обязателен для заполнения';
} else {
    // Удаляем все нецифровые символы кроме +
    $digits = preg_replace('/[^\d]/', '', $phone);
    if (strlen($digits) < 10) {
        $errors[] = 'Введите корректный номер телефона';
    }
}

// Проверка email (если указан)
if (!empty($email)) {
    if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
        $errors[] = 'Введите корректный email адрес';
    }
}

// Проверка согласия
if (!$agreement) {
    $errors[] = 'Необходимо согласие с политикой конфиденциальности';
}

// ============================================
// ОБРАБОТКА ОШИБОК
// ============================================
if (!empty($errors)) {
    // Сохраняем ошибки в сессию и возвращаем на форму
    session_start();
    $_SESSION['form_errors'] = $errors;
    header('Location: index.php#form');
    exit;
}

// ============================================
// ФОРМИРОВАНИЕ ПИСЬМА
// ============================================

// Содержимое письма в формате HTML
$message = "
<!DOCTYPE html>
<html>
<head>
    <meta charset='UTF-8'>
    <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
        .container { max-width: 600px; margin: 0 auto; padding: 20px; }
        .header { background: #1a3a5f; color: #fff; padding: 20px; text-align: center; }
        .content { padding: 20px; background: #f8f9fa; }
        .field { margin-bottom: 15px; }
        .label { font-weight: bold; color: #1a3a5f; }
        .footer { text-align: center; padding: 20px; font-size: 12px; color: #666; }
    </style>
</head>
<body>
    <div class='container'>
        <div class='header'>
            <h1>Новая заявка FOHOW</h1>
        </div>
        <div class='content'>
            <div class='field'>
                <span class='label'>Имя:</span><br>
                {$name}
            </div>
            <div class='field'>
                <span class='label'>Телефон:</span><br>
                {$phone}
            </div>
            <div class='field'>
                <span class='label'>Email:</span><br>
                " . (!empty($email) ? $email : 'Не указан') . "
            </div>
            <div class='field'>
                <span class='label'>Дата получения:</span><br>
                " . date('d.m.Y H:i:s') . "
            </div>
        </div>
        <div class='footer'>
            Заявка отправлена с сайта FOHOW
        </div>
    </div>
</body>
</html>
";

// Альтернативное текстовое содержимое (для почтовых клиентов без HTML)
$messageText = "
Новая заявка с сайта FOHOW

Имя: {$name}
Телефон: {$phone}
Email: " . (!empty($email) ? $email : 'Не указан') . "
Дата: " . date('d.m.Y H:i:s') . "
";

// ============================================
// ЗАГОЛОВКИ ПИСЬМА
// ============================================
$headers = "MIME-Version: 1.0\r\n";
$headers .= "Content-type: text/html; charset=utf-8\r\n";
$headers .= "From: FOHOW Website <noreply@fohow.ru>\r\n"; // <-- ЗАМЕНИТЕ НА ВАШ ДОМЕН
$headers .= "Reply-To: {$to}\r\n";
$headers .= "X-Mailer: PHP/" . phpversion();

// ============================================
// ОТПРАВКА ПИСЬМА
// ============================================
$mailSent = mail($to, $subject, $message, $headers);

// ============================================
// РЕДИРЕКТ ПОСЛЕ ОТПРАВКИ
// ============================================
if ($mailSent) {
    // Успешная отправка - редирект на страницу благодарности
    header('Location: thanks.html');
    exit;
} else {
    // Ошибка отправки - сохраняем ошибку и возвращаем на форму
    session_start();
    $_SESSION['form_errors'] = ['Произошла ошибка при отправке заявки. Попробуйте позже.'];
    header('Location: index.php#form');
    exit;
}
?>
