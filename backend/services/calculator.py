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
        :param base_price: Базовая цена
        :param params: Словарь параметров заказа
        :return: Итоговая стоимость (float), округленная до 2 знаков.
        """
        
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
                quantity = get_pos("quantity", 1)
                price = base_price * quantity

            elif calc_type == "area_cm2":
                length = get_pos("length")
                width = get_pos("width")
                price = (length / 10.0 * width / 10.0) * base_price

            elif calc_type == "meter_thickness":
                meters = get_pos("meters")
                thickness = get_pos("thickness", 3.0)
                if thickness == 0: thickness = 3.0
                price = meters * (base_price * (thickness / 3.0))

            elif calc_type == "per_minute":
                minutes = get_pos("minutes")
                price = minutes * base_price

            elif calc_type == "per_char":
                chars = get_pos("chars")
                price = chars * base_price

            elif calc_type == "vector_length":
                length = get_pos("length")
                price = length * base_price

            elif calc_type == "setup_batch":
                setup_price = get_pos("setup_price")
                quantity = get_pos("quantity")
                price = setup_price + (base_price * quantity)

            elif calc_type == "photo_raster":
                length = get_pos("length")
                width = get_pos("width")
                dpi_mult = get_pos("dpi_multiplier", 1.0)
                if dpi_mult == 0: dpi_mult = 1.0
                price = (length / 10.0 * width / 10.0) * base_price * dpi_mult

            elif calc_type == "cylindrical":
                diameter = get_pos("diameter")
                length = get_pos("length")
                price = (diameter * 3.14159 * length / 100.0) * base_price

            elif calc_type == "volume_3d":
                length = get_pos("length")
                width = get_pos("width")
                depth = get_pos("depth")
                price = (length / 10.0 * width / 10.0) * depth * base_price

            elif calc_type == "material_and_cut":
                length = get_pos("length")
                width = get_pos("width")
                cut_meters = get_pos("cut_meters")
                mat_cost = (length / 10.0 * width / 10.0) * base_price
                cut_cost = cut_meters * base_price
                price = mat_cost + cut_cost

            else:
                price = base_price

        except Exception as e:
            print(f"Ошибка в калькуляторе: {e}")
            return 0.0

        # Оптовые скидки
        quantity = get_pos("quantity", 1)
        discount_rate = 0.0

        if quantity >= 100: discount_rate = 0.20
        elif quantity >= 50: discount_rate = 0.15
        elif quantity >= 20: discount_rate = 0.10
        elif quantity >= 10: discount_rate = 0.05

        final_price = price * (1 - discount_rate)
        
        return round(max(0.0, final_price), 2)
