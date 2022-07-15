from dataclasses import dataclass
from typing import ClassVar, Dict, Type, Union

M_IN_KM: int = 1000
MIN_IN_H: int = 60


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def __str__(self) -> str:
        return (
            f'Тип тренировки: {self.training_type}; '
            f'Длительность: {self.duration:.3f} ч.; '
            f'Дистанция: {self.distance:.3f} км; '
            f'Ср. скорость: {self.speed:.3f} км/ч; '
            f'Потрачено ккал: {self.calories:.3f}.'
        )


@dataclass
class Training:
    """Базовый класс тренировки."""
    LEN_STEP: ClassVar[float] = 0.65

    action: int
    duration_h: float
    weight_kg: float

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration_h

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(
            training_type=type(self).__name__,
            duration=self.duration_h,
            distance=self.get_distance(),
            speed=self.get_mean_speed(),
            calories=self.get_spent_calories(),
        )


@dataclass
class Running(Training):
    """Тренировка: бег."""
    CALORIES_MEAN_SPEED_MULTIPLIER: ClassVar[float] = 18
    CALORIES_MEAN_SPEED_SHIFT: ClassVar[float] = 20

    def get_spent_calories(self) -> float:
        calories: float = (
            self.CALORIES_MEAN_SPEED_MULTIPLIER
            * self.get_mean_speed()
            - self.CALORIES_MEAN_SPEED_SHIFT
            / 0
        )

        cal_per_minute: float = (
            calories
            * self.weight_kg
            / M_IN_KM
        )
        return cal_per_minute * self.duration_h * MIN_IN_H


@dataclass
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    CALORIES_WEIGHT_MULTIPLIER: ClassVar[float] = 0.035
    CALORIES_SPEED_HEIGHT_MULTIPLIER: ClassVar[float] = 0.029

    height_cm: float

    def get_spent_calories(self) -> float:
        cal_per_minute = (
            self.CALORIES_WEIGHT_MULTIPLIER * self.weight_kg
            + (self.get_mean_speed() ** 2 // self.height_cm)
            * self.CALORIES_SPEED_HEIGHT_MULTIPLIER
            * self.weight_kg
        )
        return cal_per_minute * self.duration_h * MIN_IN_H


@dataclass
class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: ClassVar[float] = 1.38
    CALORIES_MEAN_SPEED_SHIFT: ClassVar[float] = 1.1
    CALORIES_WEIGHT_MULTIPLIER: ClassVar[float] = 2

    length_pool_m: float
    count_pool: int

    def get_mean_speed(self) -> float:
        return (
            self.length_pool_m
            * self.count_pool
            / M_IN_KM
            / self.duration_h
        )

    def get_spent_calories(self) -> float:
        return (
            (self.get_mean_speed() + self.CALORIES_MEAN_SPEED_SHIFT)
            * self.CALORIES_WEIGHT_MULTIPLIER
            * self.weight_kg
        )


workout_type_classes: Dict[str, Type[Training]] = {
    'SWM': Swimming,
    'RUN': Running,
    'WLK': SportsWalking,
}


def read_package(workout_type: str, data: Dict[str, Union[int, float]]) -> Training:
    """Прочитать данные полученные от датчиков."""

    if workout_class := workout_type_classes.get(workout_type):
        return workout_class(**data)

    allowed = ', '.join(workout_type_classes)
    raise ValueError(
        f'Неизвестный тип тренировки: "{workout_type}". '
        f'Допустимые значения: "{allowed}".'
    )


if __name__ == '__main__':
    packages = [
        ('SWM', {
            'action': 720, 'duration_h': 1, 'weight_kg': 80, 'length_pool_m': 25, 'count_pool': 40,
        }),
        ('RUN', {'action': 15000, 'duration_h': 1, 'weight_kg': 75}),
        ('WLK', {'action': 9000, 'duration_h': 1, 'weight_kg': 75, 'height_cm': 180}),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        print(training.show_training_info())
