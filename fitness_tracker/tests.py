import unittest


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
