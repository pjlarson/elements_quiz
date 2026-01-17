"""Periodic Quiz - Learn the periodic table through interactive quizzes."""

from .game import PeriodicQuiz


def main():
    """Main entry point for the CLI game."""
    quiz = PeriodicQuiz()

    print("\n" + "=" * 50)
    print("   PERIODIC TABLE QUIZ")
    print("   Learn chemical symbols and atomic numbers!")
    print("=" * 50)

    while True:
        print("\nMAIN MENU")
        print("-" * 30)
        print("1. Name → Symbol")
        print("2. Symbol → Name")
        print("3. Name → Atomic Number")
        print("4. Atomic Number → Name")
        print("5. Random Mix")
        print("6. Browse All Elements")
        print("7. Quit")
        print("-" * 30)

        choice = input("Select an option (1-7): ").strip()

        if choice == "7":
            print("\nThanks for playing! Keep learning!")
            break
        elif choice == "6":
            quiz.browse_elements()
        elif choice in quiz.MODES:
            mode_name, mode_func = quiz.MODES[choice]
            print(f"\nSelected mode: {mode_name}")

            while True:
                try:
                    num_q = input("How many questions? (default 10): ").strip()
                    num_questions = int(num_q) if num_q else 10
                    if num_questions < 1:
                        print("Please enter a positive number.")
                        continue
                    break
                except ValueError:
                    print("Please enter a valid number.")

            quiz.play_round(mode_func, num_questions)
        else:
            print("Invalid option. Please choose 1-7.")


if __name__ == "__main__":
    main()
