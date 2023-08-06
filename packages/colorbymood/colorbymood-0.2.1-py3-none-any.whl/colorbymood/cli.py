"""
entry point to the colorbymood program.
"""
import sys

from PyQt6.QtWidgets import QApplication  # pylint: disable=E0611

from colorbymood import Window
from colorbymood.color import get_hexf_from_key

def main(
) -> None:
    """
    Opens the gui window

    Args:
        hue_ (str): value for hue in the color.yaml file
        saturation_ (str): value for saturation in color.yaml file
        luminance_ (str): value for luminance in color.yaml file
        frequency_ (str): value for frequency in frequency.yaml file
    """

    def get_input():
        answer_1 = input("Hello, how may I hel you? (push/respond)\n")
        possible_responses = (
            "happyness, inspiration or excitement"
            if "push" in answer_1.lower()
            else "nervosity, sadness or distraction"
        )
        prompt = (
            f"What should I push? ({possible_responses})\n"
            if "push" in answer_1.lower()
            else f"On what should I respond? ({possible_responses})\n"
        )
        answer = input(prompt)
        try:
            assert answer in possible_responses
        except AssertionError:
            print("Wrong input given, please restart program.")
            sys.exit(0)
        return answer

    color, frequency = get_hexf_from_key(color_key=get_input())
    app = QApplication(sys.argv)
    _ = Window(
        color=color,
        frequency=frequency,
    )
    sys.exit(app.exec())
