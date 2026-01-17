"""Unit tests for the periodic quiz game."""

import pytest
from unittest.mock import patch
from periodic_quiz.game import is_close_match, PeriodicQuiz
from periodic_quiz.elements import ELEMENTS, get_element_by_symbol


class TestIsCloseMatch:
    """Tests for the fuzzy matching function."""

    def test_exact_match(self):
        """Exact matches should always return True."""
        assert is_close_match("Hydrogen", "Hydrogen") is True
        assert is_close_match("Oxygen", "Oxygen") is True
        assert is_close_match("Gold", "Gold") is True

    def test_case_insensitive(self):
        """Matching should be case-insensitive."""
        assert is_close_match("hydrogen", "Hydrogen") is True
        assert is_close_match("HYDROGEN", "Hydrogen") is True
        assert is_close_match("HyDrOgEn", "Hydrogen") is True
        assert is_close_match("oxygen", "OXYGEN") is True

    def test_whitespace_handling(self):
        """Leading/trailing whitespace should be ignored."""
        assert is_close_match("  Hydrogen  ", "Hydrogen") is True
        assert is_close_match("Oxygen ", " Oxygen") is True

    def test_transposed_letters(self):
        """Transposed letters should be accepted."""
        assert is_close_match("Hydorgen", "Hydrogen") is True
        assert is_close_match("Ocygen", "Oxygen") is True
        assert is_close_match("Sliver", "Silver") is True

    def test_missing_letter(self):
        """Missing a single letter should be accepted."""
        assert is_close_match("Hydrogn", "Hydrogen") is True
        assert is_close_match("Oxyge", "Oxygen") is True
        assert is_close_match("Calium", "Calcium") is True

    def test_extra_letter(self):
        """Extra letter should be accepted."""
        assert is_close_match("Hydrogenn", "Hydrogen") is True
        assert is_close_match("Oxygenn", "Oxygen") is True
        assert is_close_match("Telurium", "Tellurium") is True
        assert is_close_match("Telluriom", "Tellurium") is True

    def test_common_misspellings(self):
        """Common misspellings should be accepted."""
        assert is_close_match("Oxigen", "Oxygen") is True
        assert is_close_match("Calcuim", "Calcium") is True
        assert is_close_match("Pottasium", "Potassium") is True
        assert is_close_match("Magnesuim", "Magnesium") is True
        assert is_close_match("Aluminium", "Aluminum") is True
        assert is_close_match("Sulfer", "Sulfur") is True

    def test_completely_wrong(self):
        """Completely wrong answers should be rejected."""
        assert is_close_match("Iron", "Gold") is False
        assert is_close_match("Hydrogen", "Helium") is False
        assert is_close_match("Carbon", "Nitrogen") is False
        assert is_close_match("Neon", "Argon") is False

    def test_too_short(self):
        """Answers that are too short should be rejected."""
        assert is_close_match("Hyd", "Hydrogen") is False
        assert is_close_match("Ox", "Oxygen") is False
        assert is_close_match("Ca", "Calcium") is False

    def test_empty_string(self):
        """Empty strings should be rejected."""
        assert is_close_match("", "Hydrogen") is False
        assert is_close_match("   ", "Oxygen") is False

    def test_custom_threshold(self):
        """Custom threshold should be respected."""
        # With high threshold, minor typos may fail
        assert is_close_match("Hydrogn", "Hydrogen", threshold=0.95) is False
        # With low threshold, more typos accepted
        assert is_close_match("Hidrogen", "Hydrogen", threshold=0.7) is True


class TestPeriodicQuiz:
    """Tests for the PeriodicQuiz class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.quiz = PeriodicQuiz()

    def test_elements_loaded(self):
        """All 118 elements should be loaded."""
        assert len(self.quiz.elements) == 118

    def test_element_structure(self):
        """Each element should have 5 components."""
        for element in self.quiz.elements:
            assert len(element) == 5
            atomic_num, symbol, name, valence, year = element
            assert isinstance(atomic_num, int)
            assert isinstance(symbol, str)
            assert isinstance(name, str)
            assert isinstance(valence, int)
            assert isinstance(year, (int, str))

    def test_reset_score(self):
        """Score should reset to zero."""
        self.quiz.score = 10
        self.quiz.total = 15
        self.quiz.reset_score()
        assert self.quiz.score == 0
        assert self.quiz.total == 0

    def test_get_random_element(self):
        """Random element should be from the elements list."""
        for _ in range(10):
            element = self.quiz.get_random_element()
            assert element in self.quiz.elements

    def test_weights_calculated(self):
        """Weights should be calculated for all elements."""
        assert len(self.quiz._weights) == 118

    def test_pre_1946_elements_weighted_higher(self):
        """Elements discovered before 1946 should have weight 2."""
        for element, weight in zip(self.quiz.elements, self.quiz._weights):
            year = element[4]
            if year == "ancient" or (isinstance(year, int) and year < 1946):
                assert weight == 2, f"{element[2]} should have weight 2"
            else:
                assert weight == 1, f"{element[2]} should have weight 1"

    def test_weighted_selection_bias(self):
        """Pre-1946 elements should appear more frequently over many samples."""
        pre_1946_count = 0
        post_1946_count = 0
        samples = 10000

        for _ in range(samples):
            element = self.quiz.get_random_element()
            year = element[4]
            if year == "ancient" or (isinstance(year, int) and year < 1946):
                pre_1946_count += 1
            else:
                post_1946_count += 1

        # Count elements in each category
        pre_1946_elements = sum(1 for e in self.quiz.elements
                                if e[4] == "ancient" or (isinstance(e[4], int) and e[4] < 1946))
        post_1946_elements = 118 - pre_1946_elements

        # Expected ratio: (pre_1946 * 2) / (pre_1946 * 2 + post_1946 * 1)
        expected_pre_1946_ratio = (pre_1946_elements * 2) / (pre_1946_elements * 2 + post_1946_elements)
        actual_ratio = pre_1946_count / samples

        # Allow 5% tolerance for randomness
        assert abs(actual_ratio - expected_pre_1946_ratio) < 0.05, \
            f"Expected ratio ~{expected_pre_1946_ratio:.2f}, got {actual_ratio:.2f}"

    @patch('builtins.input', return_value='H')
    def test_ask_question_returns_tuple(self, mock_input):
        """ask_question should return (correct, element, mode) tuple."""
        hydrogen = (1, "H", "Hydrogen", 1, 1766)
        result = self.quiz.ask_question("name_to_symbol", hydrogen)
        assert isinstance(result, tuple)
        assert len(result) == 3
        correct, element, mode = result
        assert correct is True
        assert element == hydrogen
        assert mode == "name_to_symbol"

    @patch('builtins.input', return_value='He')
    def test_ask_question_wrong_answer_returns_false(self, mock_input):
        """ask_question should return correct=False for wrong answers."""
        hydrogen = (1, "H", "Hydrogen", 1, 1766)
        correct, element, mode = self.quiz.ask_question("name_to_symbol", hydrogen)
        assert correct is False
        assert element == hydrogen

    @patch('builtins.input', return_value='Hydrogen')
    def test_ask_question_with_specific_element(self, mock_input):
        """ask_question should use provided element instead of random."""
        hydrogen = (1, "H", "Hydrogen", 1, 1766)
        correct, element, mode = self.quiz.ask_question("symbol_to_name", hydrogen)
        assert correct is True
        assert element == hydrogen
        assert mode == "symbol_to_name"


class TestNameToSymbol:
    """Tests for name to symbol quiz mode."""

    def setup_method(self):
        self.quiz = PeriodicQuiz()

    @patch('builtins.input', return_value='H')
    def test_correct_answer(self, mock_input):
        """Correct symbol should return True."""
        hydrogen = (1, "H", "Hydrogen", 1, 1766)
        assert self.quiz.ask_name_to_symbol(hydrogen) is True

    @patch('builtins.input', return_value='h')
    def test_correct_answer_lowercase(self, mock_input):
        """Lowercase correct symbol should return True."""
        hydrogen = (1, "H", "Hydrogen", 1, 1766)
        assert self.quiz.ask_name_to_symbol(hydrogen) is True

    @patch('builtins.input', return_value='He')
    def test_wrong_answer(self, mock_input):
        """Wrong symbol should return False."""
        hydrogen = (1, "H", "Hydrogen", 1, 1766)
        assert self.quiz.ask_name_to_symbol(hydrogen) is False

    @patch('builtins.input', return_value='Au')
    def test_gold_symbol(self, mock_input):
        """Non-intuitive symbols should work."""
        gold = (79, "Au", "Gold", 1, "ancient")
        assert self.quiz.ask_name_to_symbol(gold) is True

    @patch('builtins.input', return_value='Fe')
    def test_iron_symbol(self, mock_input):
        """Latin-based symbols should work."""
        iron = (26, "Fe", "Iron", 2, "ancient")
        assert self.quiz.ask_name_to_symbol(iron) is True


class TestSymbolToName:
    """Tests for symbol to name quiz mode."""

    def setup_method(self):
        self.quiz = PeriodicQuiz()

    @patch('builtins.input', return_value='Hydrogen')
    def test_correct_answer(self, mock_input):
        """Correct name should return True."""
        hydrogen = (1, "H", "Hydrogen", 1, 1766)
        assert self.quiz.ask_symbol_to_name(hydrogen) is True

    @patch('builtins.input', return_value='hydrogen')
    def test_correct_answer_lowercase(self, mock_input):
        """Lowercase correct name should return True."""
        hydrogen = (1, "H", "Hydrogen", 1, 1766)
        assert self.quiz.ask_symbol_to_name(hydrogen) is True

    @patch('builtins.input', return_value='Hydorgen')
    def test_close_match_transposed(self, mock_input):
        """Transposed letters should return True."""
        hydrogen = (1, "H", "Hydrogen", 1, 1766)
        assert self.quiz.ask_symbol_to_name(hydrogen) is True

    @patch('builtins.input', return_value='Oxigen')
    def test_close_match_misspelling(self, mock_input):
        """Common misspelling should return True."""
        oxygen = (8, "O", "Oxygen", 6, 1774)
        assert self.quiz.ask_symbol_to_name(oxygen) is True

    @patch('builtins.input', return_value='Calcuim')
    def test_close_match_calcium(self, mock_input):
        """Misspelled Calcium should return True."""
        calcium = (20, "Ca", "Calcium", 2, 1808)
        assert self.quiz.ask_symbol_to_name(calcium) is True

    @patch('builtins.input', return_value='Helium')
    def test_wrong_answer(self, mock_input):
        """Wrong name should return False."""
        hydrogen = (1, "H", "Hydrogen", 1, 1766)
        assert self.quiz.ask_symbol_to_name(hydrogen) is False

    @patch('builtins.input', return_value='Gold')
    def test_wrong_answer_different_element(self, mock_input):
        """Completely different element should return False."""
        silver = (47, "Ag", "Silver", 1, "ancient")
        assert self.quiz.ask_symbol_to_name(silver) is False


class TestNameToNumber:
    """Tests for name to atomic number quiz mode."""

    def setup_method(self):
        self.quiz = PeriodicQuiz()

    @patch('builtins.input', return_value='1')
    def test_correct_answer(self, mock_input):
        """Correct atomic number should return True."""
        hydrogen = (1, "H", "Hydrogen", 1, 1766)
        assert self.quiz.ask_name_to_number(hydrogen) is True

    @patch('builtins.input', return_value='79')
    def test_correct_gold(self, mock_input):
        """Gold's atomic number (79) should work."""
        gold = (79, "Au", "Gold", 1, "ancient")
        assert self.quiz.ask_name_to_number(gold) is True

    @patch('builtins.input', return_value='2')
    def test_wrong_answer(self, mock_input):
        """Wrong atomic number should return False."""
        hydrogen = (1, "H", "Hydrogen", 1, 1766)
        assert self.quiz.ask_name_to_number(hydrogen) is False

    @patch('builtins.input', return_value='abc')
    def test_non_numeric_answer(self, mock_input):
        """Non-numeric input should return False."""
        hydrogen = (1, "H", "Hydrogen", 1, 1766)
        assert self.quiz.ask_name_to_number(hydrogen) is False

    @patch('builtins.input', return_value='')
    def test_empty_answer(self, mock_input):
        """Empty input should return False."""
        hydrogen = (1, "H", "Hydrogen", 1, 1766)
        assert self.quiz.ask_name_to_number(hydrogen) is False


class TestNumberToName:
    """Tests for atomic number to name quiz mode."""

    def setup_method(self):
        self.quiz = PeriodicQuiz()

    @patch('builtins.input', return_value='Hydrogen')
    def test_correct_answer(self, mock_input):
        """Correct name should return True."""
        hydrogen = (1, "H", "Hydrogen", 1, 1766)
        assert self.quiz.ask_number_to_name(hydrogen) is True

    @patch('builtins.input', return_value='hydrogen')
    def test_correct_answer_lowercase(self, mock_input):
        """Lowercase should work."""
        hydrogen = (1, "H", "Hydrogen", 1, 1766)
        assert self.quiz.ask_number_to_name(hydrogen) is True

    @patch('builtins.input', return_value='Hydorgen')
    def test_close_match(self, mock_input):
        """Typo should be accepted."""
        hydrogen = (1, "H", "Hydrogen", 1, 1766)
        assert self.quiz.ask_number_to_name(hydrogen) is True

    @patch('builtins.input', return_value='Pottasium')
    def test_close_match_potassium(self, mock_input):
        """Misspelled Potassium should return True."""
        potassium = (19, "K", "Potassium", 1, 1807)
        assert self.quiz.ask_number_to_name(potassium) is True

    @patch('builtins.input', return_value='Helium')
    def test_wrong_answer(self, mock_input):
        """Wrong name should return False."""
        hydrogen = (1, "H", "Hydrogen", 1, 1766)
        assert self.quiz.ask_number_to_name(hydrogen) is False


class TestElementsData:
    """Tests for the elements data module."""

    def test_all_elements_present(self):
        """All 118 elements should be present."""
        assert len(ELEMENTS) == 118

    def test_atomic_numbers_sequential(self):
        """Atomic numbers should be 1-118."""
        for i, element in enumerate(ELEMENTS):
            assert element[0] == i + 1

    def test_valence_electrons_valid(self):
        """Valence electrons should be 0-8."""
        for element in ELEMENTS:
            valence = element[3]
            assert 0 <= valence <= 8, f"{element[2]} has invalid valence: {valence}"

    def test_get_element_by_symbol(self):
        """Should find elements by symbol."""
        hydrogen = get_element_by_symbol("H")
        assert hydrogen is not None
        assert hydrogen[2] == "Hydrogen"

        gold = get_element_by_symbol("Au")
        assert gold is not None
        assert gold[2] == "Gold"

    def test_get_element_by_symbol_case_insensitive(self):
        """Symbol lookup should be case-insensitive."""
        assert get_element_by_symbol("h")[2] == "Hydrogen"
        assert get_element_by_symbol("AU")[2] == "Gold"
        assert get_element_by_symbol("fe")[2] == "Iron"

    def test_known_valence_electrons(self):
        """Spot check known valence electrons."""
        test_cases = [
            ("H", 1),   # Hydrogen - Group 1
            ("He", 2),  # Helium - Group 18
            ("C", 4),   # Carbon - Group 14
            ("N", 5),   # Nitrogen - Group 15
            ("O", 6),   # Oxygen - Group 16
            ("F", 7),   # Fluorine - Group 17
            ("Ne", 8),  # Neon - Group 18
            ("Na", 1),  # Sodium - Group 1
            ("Cl", 7),  # Chlorine - Group 17
        ]
        for symbol, expected_valence in test_cases:
            element = get_element_by_symbol(symbol)
            assert element[3] == expected_valence, \
                f"{element[2]} should have valence {expected_valence}, got {element[3]}"

    def test_discovery_years_valid(self):
        """Discovery years should be 'ancient' or between 1669 and 2025."""
        for element in ELEMENTS:
            year = element[4]
            if year == "ancient":
                continue
            assert 1669 <= year <= 2025, f"{element[2]} has invalid year: {year}"

    def test_known_discovery_years(self):
        """Spot check known discovery years."""
        test_cases = [
            ("Au", "ancient"),  # Gold - ancient
            ("Fe", "ancient"),  # Iron - ancient
            ("H", 1766),        # Hydrogen
            ("O", 1774),        # Oxygen
            ("Og", 2006),       # Oganesson - most recent
        ]
        for symbol, expected_year in test_cases:
            element = get_element_by_symbol(symbol)
            assert element[4] == expected_year, \
                f"{element[2]} should have year {expected_year}, got {element[4]}"

    def test_ancient_elements(self):
        """Elements known since antiquity should have 'ancient' as discovery year."""
        ancient_symbols = ["C", "S", "Fe", "Cu", "Zn", "As", "Ag", "Sn", "Sb", "Au", "Hg", "Pb", "Bi"]
        for symbol in ancient_symbols:
            element = get_element_by_symbol(symbol)
            assert element[4] == "ancient", \
                f"{element[2]} should be 'ancient', got {element[4]}"
