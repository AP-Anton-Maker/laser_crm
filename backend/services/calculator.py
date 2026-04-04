# backend/services/calculator.py

class SmartCalculator:
    @staticmethod
    def calculate(calc_type: str, base_price: float, params: dict) -> float:
        """
        Рассчитывает стоимость заказа.
        Гарантирует возврат неотрицательного числа.
        """
        price = 0.0
        
        # Безопасное извлечение чисел, замена None и негатива на 0
        def get_pos(key, default=0.0):
            val = params.get(key, default)
            return max(0.0, float(val)) if val is not None else 0.0

        try:
            if calc_type == "fixed":
                quantity = get_pos("quantity", 1)
                price = base_price * quantity

            elif calc_type == "area_cm2":
                length = get_pos("length")
                width = get_pos("width")
                # Площадь в см2 (если ввод в мм), база цена за см2
                price = (length / 10.0 * width / 10.0) * base_price

            elif calc_type == "meter_thickness":
                meters = get_pos("meters")
                thickness = get_pos("thickness", 3.0) # Дефолт 3мм, чтобы не множить на 0
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
                # Длина окружности * высота
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
                mat_price = (length / 10.0 * width / 10.0) * base_price
                cut_price = cut_meters * base_price # Предполагаем, что base_price тут за метр реза, или нужен отдельный параметр
                # По ТЗ: ((L*W)*base) + (cut*base). Если base_price разный, нужно два аргумента. 
                # Оставляем как в ТЗ, считаем base_price универсальным или усредненным.
                price = mat_price + cut_price
            
            else:
                # Неизвестный тип - возвращаем базовую цену * 1
                price = base_price

        except Exception as e:
            print(f"Ошибка калькулятора: {e}")
            return 0.0

        # Применение оптовых скидок
        quantity = get_pos("quantity", 1)
        discount_rate = 0.0
        if quantity >= 100: discount_rate = 0.20
        elif quantity >= 50: discount_rate = 0.15
        elif quantity >= 20: discount_rate = 0.10
        elif quantity >= 10: discount_rate = 0.05

        final_price = price * (1 - discount_rate)
        
        return round(max(0.0, final_price), 2)
