import unittest

from fitness_tracker.homework import InfoMessage, Training, M_IN_KM, Running


class DummyTestCase(unittest.TestCase):
    """Демонстрация работы класса TestCase."""

    @classmethod
    def setUpClass(cls) -> None:
        """Вызывается один раз перед всеми тестами, описанными в классе."""
        cls.class_level = ['c', 'l', 'a', 's', 's', 'l', 'e', 'v', 'e', 'l']

        print(f'setUpClass called: {cls.class_level}')

    def setUp(self) -> None:
        """Вызывается перед выполнением каждого теста в классе."""
        self.test_level = ['t', 'e', 's', 't', 'l', 'e', 'v', 'e', 'l']

        print(f'setUp called: {self.test_level}')

    def tearDown(self) -> None:
        """Вызывается после выполнения  каждого теста в классе."""
        print(f'tearDown called: {self.test_level}')

    @classmethod
    def tearDownClass(cls) -> None:
        """Вызывается один раз после всех тестов, описанных в классе."""
        print(f'tearDownClass called: {cls.class_level}')

    def test_test_level_append(self):
        print('test_test_level_append called')

        initial_length = len(self.test_level)
        self.test_level.append('OOPS')
        self.assertEqual(len(self.test_level), initial_length + 1)

    def test_test_level_do_nothing(self):
        print('test_test_level_do_nothing called')
        self.assertListEqual(self.test_level, ['t', 'e', 's', 't', 'l', 'e', 'v', 'e', 'l'])

    def test_class_level_append(self):
        print('test_class_level_uppercase called')

        initial_length = len(self.class_level)
        self.class_level.append('OOPS')
        self.assertEqual(len(self.class_level), initial_length + 1)

    def test_class_level_do_nothing(self):
        print('test_class_level_do_nothing called')
        self.assertListEqual(self.class_level, ['c', 'l', 'a', 's', 's', 'l', 'e', 'v', 'e', 'l'])


class InfoMessageTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.info_message = InfoMessage(
            training_type='TestTraining',
            duration=11.1111,
            distance=10.1055,
            speed=10.12,
            calories=10.1004,
        )

    def test_str(self):
        expected_str = (
            'Тип тренировки: TestTraining; '
            'Длительность: 11.111 ч.; '
            'Дистанция: 10.105 км; '
            'Ср. скорость: 10.120 км/ч; '
            'Потрачено ккал: 10.100.'
        )
        self.assertEqual(str(self.info_message), expected_str)


class TestTraining(Training):
    """Наследник класса Training, нужен чтобы протестировать базовый функционал:

    * get_distance - правильность расчетов
    * get_mean_speed - правильность расчетов
    * show_training_info - возвращается InfoMessage с правильным именем класса

    """

    def get_spent_calories(self) -> float:
        """Простейшая реализация абстрактного метода."""
        return 100


class TrainingTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.training = TestTraining(
            action=100,
            duration_h=0.5,
            weight_kg=82.7,
        )
        cls.expected_distance = 100 * TestTraining.LEN_STEP / M_IN_KM
        cls.expected_speed = cls.expected_distance / 0.5

    def test_get_distance(self):
        self.assertEqual(self.training.get_distance(), self.expected_distance)

    def test_get_mean_speed(self):
        self.assertEqual(self.training.get_mean_speed(), self.expected_speed)

    def test_show_training_info(self):
        info_msg = self.training.show_training_info()
        self.assertIn(TestTraining.__name__, str(info_msg))


class RunningTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.running = Running(
            action=15000,
            duration_h=1,
            weight_kg=75,
        )

    def test_catch_zero_division(self):
        """Тест для быстрого поиска непредвиденной ошибки.

        Как только проблема устранена, тест перестает проходить успешно, и значит можно его удалить

        """
        with self.assertRaises(ZeroDivisionError):
            self.running.show_training_info()
