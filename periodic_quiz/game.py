"""Game logic for the periodic table quiz."""

import random
from difflib import SequenceMatcher
from .elements import ELEMENTS


def is_close_match(answer: str, correct: str, threshold: float = 0.8) -> bool:
    """Check if answer is close enough to correct (allows small typos)."""
    answer = answer.lower().strip()
    correct = correct.lower().strip()

    if answer == correct:
        return True

    ratio = SequenceMatcher(None, answer, correct).ratio()
    return ratio >= threshold


class PeriodicQuiz:
    """Quiz game for learning the periodic table."""

    MODES = {
        "1": ("Name → Symbol", "name_to_symbol"),
        "2": ("Symbol → Name", "symbol_to_name"),
        "3": ("Name → Atomic Number", "name_to_number"),
        "4": ("Atomic Number → Name", "number_to_name"),
        "5": ("Random Mix", "random"),
    }

    def __init__(self):
        self.score = 0
        self.total = 0
        self.elements = list(ELEMENTS)
        self._weights = self._calculate_weights()

    def _calculate_weights(self) -> list:
        """Calculate selection weights. Elements discovered before 1946 are twice as likely."""
        weights = []
        for element in self.elements:
            year = element[4]
            if year == "ancient" or (isinstance(year, int) and year < 1946):
                weights.append(2)
            else:
                weights.append(1)
        return weights

    def reset_score(self):
        """Reset the score counters."""
        self.score = 0
        self.total = 0

    def get_random_element(self) -> tuple:
        """Get a random element, weighted so pre-1946 elements are twice as likely."""
        return random.choices(self.elements, weights=self._weights, k=1)[0]

    def ask_name_to_symbol(self, element: tuple) -> bool:
        """Ask user to provide symbol given the element name."""
        atomic_num, symbol, name, valence, year = element
        print(f"\nWhat is the chemical symbol for {name}?")
        answer = input("Your answer: ").strip()

        if answer.lower() == symbol.lower():
            print(f"Correct! {name} = {symbol} (valence: {valence}, discovered: {year})")
            return True
        else:
            print(f"Incorrect. The symbol for {name} is {symbol} (valence: {valence}, discovered: {year})")
            return False

    def ask_symbol_to_name(self, element: tuple) -> bool:
        """Ask user to provide name given the symbol."""
        atomic_num, symbol, name, valence, year = element
        print(f"\nWhat element has the symbol {symbol}?")
        answer = input("Your answer: ").strip()

        if answer.lower() == name.lower():
            print(f"Correct! {symbol} = {name} (valence: {valence}, discovered: {year})")
            return True
        elif is_close_match(answer, name):
            print(f"Close enough! {symbol} = {name} (valence: {valence}, discovered: {year}) (you typed: {answer})")
            return True
        else:
            print(f"Incorrect. {symbol} is the symbol for {name} (valence: {valence}, discovered: {year})")
            return False

    def ask_name_to_number(self, element: tuple) -> bool:
        """Ask user to provide atomic number given the element name."""
        atomic_num, symbol, name, valence, year = element
        print(f"\nWhat is the atomic number of {name}?")
        answer = input("Your answer: ").strip()

        try:
            if int(answer) == atomic_num:
                print(f"Correct! {name} has atomic number {atomic_num} (valence: {valence}, discovered: {year})")
                return True
        except ValueError:
            pass

        print(f"Incorrect. {name} has atomic number {atomic_num} (valence: {valence}, discovered: {year})")
        return False

    def ask_number_to_name(self, element: tuple) -> bool:
        """Ask user to provide element name given the atomic number."""
        atomic_num, symbol, name, valence, year = element
        print(f"\nWhat element has atomic number {atomic_num}?")
        answer = input("Your answer: ").strip()

        if answer.lower() == name.lower():
            print(f"Correct! Atomic number {atomic_num} is {name} (valence: {valence}, discovered: {year})")
            return True
        elif is_close_match(answer, name):
            print(f"Close enough! Atomic number {atomic_num} is {name} (valence: {valence}, "
                  f"discovered: {year}) (you typed: {answer})")
            return True
        else:
            print(f"Incorrect. Atomic number {atomic_num} is {name} ({symbol}, valence: {valence}, discovered: {year})")
            return False

    def ask_question(self, mode: str, element: tuple = None) -> tuple:
        """Ask a question based on the selected mode.

        Returns (correct: bool, element: tuple, actual_mode: str) for retry tracking.
        """
        if element is None:
            element = self.get_random_element()

        actual_mode = mode
        if mode == "random":
            actual_mode = random.choice(["name_to_symbol", "symbol_to_name",
                                         "name_to_number", "number_to_name"])

        if actual_mode == "name_to_symbol":
            correct = self.ask_name_to_symbol(element)
        elif actual_mode == "symbol_to_name":
            correct = self.ask_symbol_to_name(element)
        elif actual_mode == "name_to_number":
            correct = self.ask_name_to_number(element)
        elif actual_mode == "number_to_name":
            correct = self.ask_number_to_name(element)
        else:
            correct = False

        return (correct, element, actual_mode)

    def play_round(self, mode: str, num_questions: int = 10):
        """Play a round of the quiz."""
        self.reset_score()
        missed_questions = []  # List of (element, actual_mode) tuples to retry

        print(f"\n{'=' * 50}")
        print(f"Starting quiz with {num_questions} questions!")
        print(f"{'=' * 50}")

        for i in range(num_questions):
            print(f"\n--- Question {i + 1}/{num_questions} ---")
            correct, element, actual_mode = self.ask_question(mode)
            if correct:
                self.score += 1
            else:
                missed_questions.append((element, actual_mode))
            self.total += 1
            print(f"Score: {self.score}/{self.total}")

        # Retry missed questions
        if missed_questions:
            print(f"\n{'=' * 50}")
            print(f"RETRY: {len(missed_questions)} missed question(s)")
            print(f"{'=' * 50}")

            retry_round = 1
            while missed_questions:
                print(f"\n--- Retry Round {retry_round} ---")
                still_missed = []

                for i, (element, actual_mode) in enumerate(missed_questions):
                    print(f"\n[Retry {i + 1}/{len(missed_questions)}]")
                    correct, _, _ = self.ask_question(actual_mode, element)
                    if correct:
                        self.score += 1
                    else:
                        still_missed.append((element, actual_mode))
                    self.total += 1
                    print(f"Score: {self.score}/{self.total}")

                missed_questions = still_missed
                retry_round += 1

        self.show_final_score()

    def show_final_score(self):
        """Display the final score."""
        percentage = (self.score / self.total * 100) if self.total > 0 else 0

        print(f"\n{'=' * 50}")
        print("QUIZ COMPLETE!")
        print(f"{'=' * 50}")
        print(f"Final Score: {self.score}/{self.total} ({percentage:.1f}%)")

        if percentage == 100:
            print("Perfect score! You're a periodic table master!")
        elif percentage >= 80:
            print("Excellent work! Keep practicing!")
        elif percentage >= 60:
            print("Good effort! Room for improvement.")
        elif percentage >= 40:
            print("Keep studying! You'll get there.")
        else:
            print("Time to hit the books! Practice makes perfect.")
        print()

    def browse_elements(self):
        """Browse all elements in the periodic table."""
        print(f"\n{'=' * 70}")
        print("PERIODIC TABLE OF ELEMENTS")
        print(f"{'=' * 70}")
        print(f"{'#':<4} {'Symbol':<6} {'Name':<15} {'Valence':<8} {'Discovered':<10}")
        print("-" * 70)

        for atomic_num, symbol, name, valence, year in self.elements:
            print(f"{atomic_num:<4} {symbol:<6} {name:<15} {valence:<8} {year:<10}")

        print(f"\nTotal: {len(self.elements)} elements")
        input("\nPress Enter to continue...")
