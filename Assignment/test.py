
import unittest

from cat import Cat

class CatTests(unittest.TestCase):
    def test_initial_age(self):
        cat = Cat()
        self.assertGreaterEqual(cat.age, 5)  # Assert initial age is greater than or equal to 5
        self.assertLessEqual(cat.age, 10)    # Assert initial age is less than or equal to 10

    def test_speak_method(self):
        cat = Cat()
        cat.setAge(6)
        # Assert age increases by 1 after speaking
        cat.speak("Meow")                      
        self.assertEqual(cat.age, 7)        # Assert age still increases by 1

    def test_set_name(self):
        cat = Cat()
        cat.setName("Whiskers")
        self.assertEqual(cat.name, "Whiskers")   # Assert name is properly set
        self.assertIn("Whiskers", cat.getNames()) # Assert name is added to name history

    def test_average_name_length(self):
        cat = Cat()
        cat.setName("Fluffy")
        cat.setName("Mittens")
        self.assertEqual(cat.getAverageNameLength(), 6.5)  # Assert average name length is calculated correctly

if __name__ == "__main__":
    unittest.main()