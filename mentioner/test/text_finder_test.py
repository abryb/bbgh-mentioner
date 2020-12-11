import unittest

from mentioner.finder import TextFinder
from mentioner.morfeusz import morfeusz_wrapper

finder = TextFinder(morfeusz_wrapper)

class FinderTestCase(unittest.TestCase):
    def test_can_find_name_and_lastname(self):
        text = """
        7 listopada 2020, 15:00 - Mielec (stadion MOSiR) Stal Mielec 0-1 Warta Poznań Mateusz Kuzimski 88 Stal: 13. 
        Rafał Strączek - 11. Szymon Stasik, 14. Kamil Kościelny, 4. Bożidar Czorbadżijski (58, 98. Paweł Tomczyk), 
        23. Krystian Getinger - 10. Mateusz Mak, 21. Mateusz Matras, 20. Grzegorz Tomasiewicz (81, 27. Damian Pawłowski),
        17. Petteri Forsell, 7. Maciej Domański (65, 96. Robert Dadok) - 77. Jakub Wróbel (81, 99. Łukasz Zjawiński). 
        Warta: 33. Daniel Bielica - 23. Mateusz Spychała, 5. Bartosz Kieliba, 4. Robert Ivanov, 13. Jakub Kuzdra - 
        18. Mario Rodríguez (34, 25. Gracjan Jaroch; 46, 2. Jan Grzesik), 6. Łukasz Trałka, 21. Mateusz Kupczak, 
        17. Mateusz Czyżycki (39, 3. Jakub Kiełb), 11. Michał Jakóbowski - 9. Mateusz Kuzimski. żółte kartki: Matras, 
        Stasik - Czyżycki. czerwona kartka: Mateusz Spychała (34. minuta, Warta, za faul taktyczny). sędziował: 
        Sebastian Jarzębak (Bytom). Mecz bez udziału publiczności.
         """
        text = text.replace("\n", " ")
        result = finder.find_full_names(text)
        full_names = [r.result.full_name() for r in result]
        self.assertIn(u"Jakub Wróbel", full_names)
        self.assertIn(u"Paweł Tomczyk", full_names)
        self.assertIn(u"Damian Pawłowski", full_names)
        self.assertIn(u"Mateusz Matras", full_names)


    def test_can_find_last_name(self):
        text = """
        trener nie ma nic do powiedzenia. nawet Mourinio nie wygrałby meczu z takimi asami jak Wróbel, Tomczyk, 
        Pawłowski, Matras... te piłkarzyny w drugiej lidze by miejsca nie znalazły. tu trzeba mieć pretensje do 
        dyrektora sportowego i zarządu! Mielec pierwsza liga wita.
        """
        result = finder.find_last_names(text)
        last_names = [r.result for r in result]
        self.assertIn("Wróbel", last_names)
        self.assertIn("Tomczyk", last_names)
        self.assertIn("Pawłowski", last_names)
        self.assertIn("Matras", last_names)

    def test_can_find_lower_case_letter_last_name(self):
        self.assertGreater(len(finder.find_last_names("Co za Kowalski!")), 0)


if __name__ == '__main__':
    unittest.main()
