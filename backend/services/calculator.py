import enum
from pydantic import BaseModel
from typing import Optional
from core.config import settings

class CalcMethod(str, enum.Enum):
    fixed = "fixed"
    area_cm2 = "area_cm2"
    meter_thickness = "meter_thickness"
    per_minute = "per_minute"
    per_char = "per_char"
    vector_length = "vector_length"
    setup_batch = "setup_batch"
    photo_raster = "photo_raster"
    cylindrical = "cylindrical"
    volume_3d = "volume_3d"
    complex = "complex"

class CalculatorParams(BaseModel):
    method: CalcMethod
    base_price: float
    quantity: int = 1
    is_urgent: bool = False
    
    # Специфичные параметры (могут быть None для других методов)
    width_mm: Optional[float] = 0.0
    height_mm: Optional[float] = 0.0
    meters_cut: Optional[float] = 0.0
    thickness_mm: Optional[float] = 0.0
    minutes: Optional[float] = 0.0
    char_count: Optional[int] = 0
    vector_length_m: Optional[float] = 0.0
    setup_price: Optional[float] = 0.0
    dpi_coeff: Optional[float] = 1.0
    diameter_mm: Optional[float] = 0.0
    length_mm: Optional[float] = 0.0
    depth_mm: Optional[float] = 0.0
    material_area_cm2: Optional[float] = 0.0
    material_price: Optional[float] = 0.0


class CalculatorService:
    @staticmethod
    def calculate(params: CalculatorParams) -> float:
        """
        Расчет стоимости по 11 алгоритмам с защитой от демпинга и наценкой за срочность.
        """
        total = 0.0
        
        # 1. Штучный товар (Фиксированная цена)
        if params.method == CalcMethod.fixed:
            total = params.base_price * params.quantity
            
        # 2. Площадь в см2 (Шильды, гравировка дерева)
        elif params.method == CalcMethod.area_cm2:
            area = (params.width_mm / 10) * (params.height_mm / 10)
            total = area * params.base_price * params.quantity
            
        # 3. Метры реза с учетом толщины (Резка фанеры)
        elif params.method == CalcMethod.meter_thickness:
            multiplier = params.thickness_mm / 3.0 if params.thickness_mm > 0 else 1.0
            total = params.meters_cut * (params.base_price * multiplier) * params.quantity
            
        # 4. Поминутная тарификация (Долгая гравировка MOPA/JPT)
        elif params.method == CalcMethod.per_minute:
            total = params.minutes * params.base_price * params.quantity
            
        # 5. Посимвольно (Кольца, ручки)
        elif params.method == CalcMethod.per_char:
            total = params.char_count * params.base_price * params.quantity
            
        # 6. Длина вектора (Промышленная резка)
        elif params.method == CalcMethod.vector_length:
            total = params.vector_length_m * params.base_price * params.quantity
            
        # 7. Настройка станка + Тираж (B2B опт)
        elif params.method == CalcMethod.setup_batch:
            total = params.setup_price + (params.base_price * params.quantity)
            
        # 8. Растровая гравировка (Фото на дереве)
        elif params.method == CalcMethod.photo_raster:
            area = (params.width_mm / 10) * (params.height_mm / 10)
            total = area * params.base_price * params.dpi_coeff * params.quantity
            
        # 9. Цилиндрическая гравировка (Поворотная ось: термосы, кружки)
        elif params.method == CalcMethod.cylindrical:
            # Площадь цилиндра: Пи * Диаметр * Длина (в см)
            cylinder_area = 3.14 * (params.diameter_mm / 10) * (params.length_mm / 10)
            total = cylinder_area * params.base_price * params.quantity
            
        # 10. 3D Выборка (Глубокое клише)
        elif params.method == CalcMethod.volume_3d:
            area = (params.width_mm / 10) * (params.height_mm / 10)
            total = area * params.depth_mm * params.base_price * params.quantity
            
        # 11. Комбинированный: Материал + Рез
        elif params.method == CalcMethod.complex:
            material_cost = params.material_area_cm2 * params.material_price
            cut_cost = params.meters_cut * params.base_price
            total = (material_cost + cut_cost) * params.quantity

        # Наценка за срочность (x1.5)
        if params.is_urgent:
            total *= 1.5
            
        # Защита от минимальной стоимости
        if total < settings.MIN_ORDER_PRICE:
            total = float(settings.MIN_ORDER_PRICE)
            
        return round(total, 2)
