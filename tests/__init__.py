import unittest
from dotenv_manager import EnvManager

class TestStringMethods(unittest.TestCase):

    def test_str(self):
        @EnvManager(strict=True)
        class CONFIG:
            STR_KEY1: str
            STR_KEY2: str
        self.assertEqual(CONFIG.STR_KEY1, "KEY1_VALUE")
        self.assertEqual(CONFIG.STR_KEY2, "KEY2_VALUE")

    def test_int(self):
        @EnvManager(strict=True)
        class CONFIG:
            INT_KEY3: int
        self.assertEqual(CONFIG.INT_KEY3, 3)

    def test_float(self):
        @EnvManager(strict=True)
        class CONFIG:
            FLOAT_KEY4: float
        self.assertEqual(CONFIG.FLOAT_KEY4, 4.2)

    def test_prefix(self):
        @EnvManager(prefix="STR_", strict=True)
        class CONFIG:
            KEY1: str
            KEY2: str
        self.assertEqual(CONFIG.KEY1, "KEY1_VALUE")
        self.assertEqual(CONFIG.KEY2, "KEY2_VALUE")

    def test_not_found(self):
        @EnvManager(strict=False)
        class CONFIG:
            KEY_NOT_FOUND: str
        with self.assertRaises(AttributeError):
            CONFIG.KEY_NOT_FOUND

    def test_wrong_type_str(self):
        @EnvManager(strict=False)
        class CONFIG:
            STR_KEY2: int
        with self.assertRaises(AttributeError):
            CONFIG.STR_KEY2

    def test_wrong_type_float(self):
        @EnvManager(strict=False)
        class CONFIG:
            FLOAT_KEY4: int
        with self.assertRaises(AttributeError):
            CONFIG.FLOAT_KEY4
    
    def test_strict(self):
        with self.assertRaises(ValueError):
            @EnvManager(strict=True)
            class CONFIG:
                FLOAT_KEY4: int
        with self.assertRaises(AttributeError):
            @EnvManager(strict=True)
            class CONFIG:
                KEY_NOT_FOUND: str

if __name__ == '__main__':
    unittest.main()
