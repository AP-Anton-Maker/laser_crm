from typing import Dict, Any


class SmartCalculator:
    """
    Умный калькулятор для расчета стоимости заказов лазерной резки и гравировки.
    Реализует 11 алгоритмов расчета согласно ТЗ.
    Гарантирует защиту от деления на ноль и отрицательных значений.
    """

    @staticmethod
    def calculate(calc_type: str, base_price: float, params: Dict[str, Any]) -> float:
        """
        Основной метод расчета.
        
        :param calc_type: Тип расчета (fixed, area_cm2, meter_thickness и т.д.)
        :param base_price: Базовая цена (за шт, за м2, за минуту и т.д.)
        :param params: Словарь параметров заказа (длина, ширина, количество и т.д.)
        :return: Итоговая стоимость (float), округленная до 2 знаков.
        """
        
        # Внутренняя функция для безопасного получения положительных чисел
        def get_pos(key: str, default: float = 0.0) -> float:
            val = params.get(key, default)
            if val is None:
                return default
            try:
                v = float(val)
                return max(0.0, v)
            except (ValueError, TypeError):
                return default

        price = 0.0

        try:
            if calc_type == "fixed":
                # Штучный товар: цена * количество
                quantity = get_pos("quantity", 1)
                price = base_price * quantity

            elif calc_type == "area_cm2":
                # Площадь в см2: (L/10 * W/10) * цена_за_м2
                length = get_pos("length")
                width = get_pos("width")
                price = (length / 10.0 * width / 10.0) * base_price

            elif calc_type == "meter_thickness":
                # Резка фанеры с учетом толщины: метры * (база * (толщина / 3))
                meters = get_pos("meters")
                thickness = get_pos("thickness", 3.0)
                if thickness == 0:
                    thickness = 3.0  # Защита от деления на ноль в логике коэффициента
                price = meters * (base_price * (thickness / 3.0))

            elif calc_type == "per_minute":
                # Долгая гравировка: минуты * цена_за_минуту
                minutes = get_pos("minutes")
                price = minutes * base_price

            elif calc_type == "per_char":
                # Гравировка текста: символы * цена_за_символ
                chars = get_pos("chars")
                price = chars * base_price

            elif calc_type == "vector_length":
                # Промышленная резка: длина вектора * цена_за_метр
                length = get_pos("length")
                price = length * base_price

            elif calc_type == "setup_batch":
                # Тираж с настройкой: настройка + (цена_шт * кол-во)
                setup_price = get_pos("setup_price")
                quantity = get_pos("quantity")
                price = setup_price + (base_price * quantity)

            elif calc_type == "photo_raster":
                # Фото на дереве: площадь * база * dpi_multiplier
                length = get_pos("length")
                width = get_pos("width")
                dpi_mult = get_pos("dpi_multiplier", 1.0)
                if dpi_mult == 0:
                    dpi_mult = 1.0
                price = (length / 10.0 * width / 10.0) * base_price * dpi_mult

            elif calc_type == "cylindrical":
                # Ось/Кружки: (диаметр * Пи * длина/100) * база
                diameter = get_pos("diameter")
                length = get_pos("length")
                price = (diameter * 3.14159 * length / 100.0) * base_price

            elif calc_type == "volume_3d":
                # 3D-клише: (L/10 * W/10) * глубина * база
                length = get_pos("length")
                width = get_pos("width")
                depth = get_pos("depth")
                price = (length / 10.0 * width / 10.0) * depth * base_price

            elif calc_type == "material_and_cut":
                # Материал + Резка: (площадь_материала * цена_листа) + (длина_реза * цена_реза)
                length = get_pos("length")
                width = get_pos("width")
                cut_meters = get_pos("cut_meters")
                
                mat_cost = (length / 10.0 * width / 10.0) * base_price
                cut_cost = cut_meters * base_price # Здесь база может быть ценой реза, если передана отдельно
                # В упрощенной модели считаем, что base_price участвует в обоих или параметры разные
                # Для гибкости предположим, что для реза есть свой параметр в базе или используем тот же
                price = mat_cost + cut_cost

            else:
                # Неизвестный тип - возвращаем базовую цену как минимальную
                price = base_price

        except Exception as e:
            print(f"Ошибка в калькуляторе: {e}")
            return 0.0

        # Применение оптовых скидок
        quantity = get_pos("quantity", 1)
        discount_rate = 0.0

        if quantity >= 100:
            discount_rate = 0.20
        elif quantity >= 50:
            discount_rate = 0.15
        elif quantity >= 20:
            discount_rate = 0.10
        elif quantity >= 10:
            discount_rate = 0.05

        final_price = price * (1 - discount_rate)
        
        # Возвращаем неотрицательное число, округленное до 2 знаков
        return round(max(0.0, final_price), 2)
