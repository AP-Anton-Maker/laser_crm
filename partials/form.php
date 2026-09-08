<!-- 
    НАЧАЛО СЕКЦИИ FORM (ФОРМА ЗАХВАТА)
    Форма для сбора заявок с валидацией
-->
<section class="form-section section" id="form">
    <div class="container">
        <!-- ЗАГОЛОВОК H2 -->
        <!-- ТЕКСТ ДЛЯ РЕДАКТИРОВАНИЯ -->
        <h2 class="section-title">Время действовать! Сделай свой выбор <span>в пользу успеха</span></h2>
        
        <!-- КОНТЕНТ ФОРМЫ -->
        <div class="form-content">
            <!-- ПРИЗЫВ К ДЕЙСТВИЮ -->
            <!-- ТЕКСТ ДЛЯ РЕДАКТИРОВАНИЯ -->
            <p>Оставьте заявку прямо сейчас и получите персональную консультацию от нашего менеджера. Мы поможем вам сделать первый шаг к финансовой независимости!</p>
            
            <!-- ФОРМА -->
            <!-- Отправляется методом POST на send.php -->
            <form class="contact-form" id="contactForm" action="send.php" method="POST">
                <!-- ПОЛЕ: Имя (обязательное) -->
                <div class="form-group">
                    <label class="form-label" for="name">Ваше имя *</label>
                    <!-- ТЕКСТ ДЛЯ РЕДАКТИРОВАНИЯ: placeholder -->
                    <input type="text" id="name" name="name" class="form-input" placeholder="Иван Иванов" required>
                </div>
                
                <!-- ПОЛЕ: Телефон (обязательное, с маской) -->
                <div class="form-group">
                    <label class="form-label" for="phone">Номер телефона *</label>
                    <!-- ТЕКСТ ДЛЯ РЕДАКТИРОВАНИЯ: placeholder -->
                    <input type="tel" id="phone" name="phone" class="form-input" placeholder="+7 (___) ___-__-__" required>
                </div>
                
                <!-- ПОЛЕ: Email (необязательное) -->
                <div class="form-group">
                    <label class="form-label" for="email">Email (необязательно)</label>
                    <!-- ТЕКСТ ДЛЯ РЕДАКТИРОВАНИЯ: placeholder -->
                    <input type="email" id="email" name="email" class="form-input" placeholder="example@mail.ru">
                </div>
                
                <!-- ЧЕКБОКС: Согласие с политикой конфиденциальности (обязательный) -->
                <div class="form-checkbox">
                    <input type="checkbox" id="agreement" name="agreement" required>
                    <!-- ТЕКСТ ДЛЯ РЕДАКТИРОВАНИЯ -->
                    <label for="agreement">Я согласен с <a href="#" target="_blank">политикой конфиденциальности</a> и даю согласие на обработку персональных данных *</label>
                </div>
                
                <!-- КНОПКА ОТПРАВКИ -->
                <!-- ТЕКСТ ДЛЯ РЕДАКТИРОВАНИЯ -->
                <button type="submit" class="form-submit">Хочу на собеседование</button>
            </form>
            
            <!-- ВИДЕО ПОД ФОРМОЙ -->
            <div class="form-video">
                <!-- ВИДЕО-ЗАГЛУШКА: Замените на реальное видео -->
                <!-- ЗДЕСЬ ВСТАВЬТЕ СВОЁ ВИДЕО -->
                <div class="video-placeholder">
                    <div class="video-poster">
                        <div class="play-icon">
                            <div class="play-triangle"></div>
                        </div>
                        <!-- ПОДПИСЬ ПОД ВИДЕО -->
                        <!-- ТЕКСТ ДЛЯ РЕДАКТИРОВАНИЯ -->
                        <p class="video-caption">Узнайте больше о возможностях FOHOW</p>
                    </div>
                </div>
                <!-- 
                    КАК ЗАМЕНИТЬ НА РЕАЛЬНОЕ ВИДЕО:
                    1. YouTube/Vimeo iframe:
                    <iframe src="https://www.youtube.com/embed/ВАШ_ID" frameborder="0" allowfullscreen style="width:100%;height:100%;border-radius:12px;"></iframe>
                    
                    2. Локальное video:
                    <video controls style="width:100%;border-radius:12px;">
                        <source src="video/form.mp4" type="video/mp4">
                    </video>
                -->
            </div>
        </div>
    </div>
</section>
<!-- КОНЕЦ СЕКЦИИ FORM -->
