<?php
/**
 * FOHOW Landing Page - Главная страница (index.php)
 * Собирает все секции через include из папки partials/
 * 
 * ИНСТРУКЦИЯ ПО ИСПОЛЬЗОВАНИЮ:
 * 1. Загрузите все файлы на хостинг с поддержкой PHP
 * 2. Убедитесь, что структура папок сохранена
 * 3. Откройте сайт в браузере
 */
?>
<!DOCTYPE html>
<html lang="ru">
<head>
    <!-- МЕТА-ТЕГИ -->
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    
    <!-- SEO: Заголовок и описание -->
    <!-- ТЕКСТ ДЛЯ РЕДАКТИРОВАНИЯ -->
    <title>FOHOW — Твой путь к успеху | Высоковольтное оборудование и бизнес с Китаем</title>
    <meta name="description" content="Присоединяйтесь к команде FOHOW! Продажа высоковольтного оборудования, уникальная бизнес-возможность, обучение и поддержка партнёров.">
    <meta name="keywords" content="FOHOW, бизнес, партнёрство, высокотехнологичные продукты, здоровье, доход">
    
    <!-- ШРИФТЫ: Google Fonts Inter -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    
    <!-- СТИЛИ: Подключение CSS -->
    <link rel="stylesheet" href="css/style.css">
    
    <!-- FAVICON: Замените на реальную иконку -->
    <!-- ССЫЛКА НА ИЗОБРАЖЕНИЕ: img/favicon.ico -->
    <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 40 40'><circle cx='20' cy='20' r='20' fill='%23f5a623'/><text x='20' y='27' font-family='Arial' font-size='20' font-weight='bold' fill='%231a3a5f' text-anchor='middle'>F</text></svg>">
</head>
<body>
    <!-- ШАПКА -->
    <?php include 'partials/header.php'; ?>
    
    <main>
        <!-- ГЕРОЙ (ГЛАВНЫЙ ЭКРАН) -->
        <?php include 'partials/hero.php'; ?>
        
        <!-- О БИЗНЕСЕ -->
        <?php include 'partials/about.php'; ?>
        
        <!-- ПРЕИМУЩЕСТВА -->
        <?php include 'partials/advantages.php'; ?>
        
        <!-- СПОСОБЫ ЗАРАБОТКА -->
        <?php include 'partials/earnings.php'; ?>
        
        <!-- ОТЗЫВЫ -->
        <?php include 'partials/testimonials.php'; ?>
        
        <!-- КАК НАЧАТЬ (ШАГИ) -->
        <?php include 'partials/steps.php'; ?>
        
        <!-- FAQ (ВОПРОСЫ И ОТВЕТЫ) -->
        <?php include 'partials/faq.php'; ?>
        
        <!-- ФОРМА ЗАХВАТА -->
        <?php include 'partials/form.php'; ?>
    </main>
    
    <!-- ПОДВАЛ -->
    <?php include 'partials/footer.php'; ?>
    
    <!-- СКРИПТЫ: Подключение JavaScript -->
    <script src="js/script.js"></script>
</body>
</html>
