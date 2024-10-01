import pandas as pd
import random

from shared.generic import loose_string_equal
from shared.interface import Interface


RAND_DATA_PATH = "data/data.csv"
ONEK_WORDS_PATH = "data/1kwords.csv"


class ProblemState:
    """
    Used to track the upcoming problem.

    Players will need to solve problems to increase their score
    """

    def __init__(self) -> None:
        self.problem = ""
        self.solution = ""
        self.set_size = ""

    def set(self, problem, solution, set_size):
        self.problem = problem
        self.solution = solution
        self.set_size = set_size

        return self


class GameState:
    """
    Class used to track the state of various mechanics and interactions
    """

    def __init__(self) -> None:

        self.streak = 0
        self.high_score = 0
        self.low_score = 0
        self.last_translation = None
        self.last_answer = None
        self.previous_correct = None
        self.words = 0

    def set_words(self, set_size):

        self.words = set_size

    def correct_answer(self):
        """
        Invoked by the engine to inform the state of a correct answer.
        """

        self.streak += 1
        if self.high_score < self.streak:
            self.high_score += 1
        self.low_score = 0

    def incorrect_answer(self):
        """
        Invoked by the engine to inform the state of a correct answer.
        """

        if self.high_score < self.streak:
            self.high_score = self.streak
        self.streak = 0
        self.low_score += 1

    def next_question(self, translation, answer, previous_correct: bool):

        self.last_translation = translation
        self.last_answer = answer
        self.previous_correct = previous_correct


class GameEngine:

    def __init__(self) -> None:

        self.game_state = GameState()

        self.problem = ProblemState()

        # check the desired game mode
        self.mode = Interface(self.game_state, self.problem).onek_question()

        # get the user provided config
        self.config = self.game_mode_manager()

        # set up all of the data that we need
        self.translation_data = self.get_cleaned_data()

        self.game_state.set_words(self.translation_data.shape[0])

        # manage the game session
        self.session = self.game_engine()

    def game_mode_manager(self) -> dict:
        """
        Function which manages the game mode and difficulty of a given class.

        @ returns -> dict
        mode_config = {
            "1k_version": None,
            "difficulty": None
        }
        """

        # hold the defaults for later
        mode_config = {"1k_version": None, "difficulty": None}

        # Check if they want to play the 1k mode
        if loose_string_equal(self.mode, "y"):

            mode_config["1k_version"] = True
            mode_config["difficulty"] = int(
                input("how many words would you like? (0-n): ")
            )
            mode_config["difficulty_again"] = int(
                input("What length should they be below? (1-n): ")
            )

            return mode_config
        # else put them into the wider mode
        else:
            mode_config["difficulty"] = int(
                input("How many words should we use? (0-1000): ")
            )
            mode_config["1k_version"] = False

            return mode_config

    def get_cleaned_data(self) -> pd.DataFrame:
        """
        Get the source data that we need to

        returns: DataFrame
            [ english, spanish ]
        """

        if self.mode == "n":
            frame = pd.read_csv(RAND_DATA_PATH)

            # return a subset of the data based on count of spaces and user input
            filtered_df = frame[
                frame["spanish"].str.count(" ")
                <= self.config["difficulty"] & frame["english"].str.count(" ")
                <= self.config["difficulty"]
            ]
        elif self.mode == "y":
            frame = pd.read_csv(ONEK_WORDS_PATH)[0 : self.config["difficulty"]]

            filtered_frame = frame[
                frame["spanish"].str.len() <= self.config["difficulty_again"]
            ]

            filtered_df = filtered_frame[0 : self.config["difficulty"]]

        return filtered_df

    def setup_problem_state(self) -> dict:
        """
        Will return a single translation problem from the target data.
        """

        # needed for the RNG out
        set_size = self.translation_data.shape[0] - 1

        # TODO: upgrade selection process
        random_row = random.randint(0, set_size)

        # we want to hold the selected row
        row_content = self.translation_data.iloc[random_row].values

        # gets the row in the target language
        problem = row_content[1]

        # gets the row in the user language
        solution = row_content[0]

        return self.problem.set(problem, solution, set_size)

    def game_engine(self) -> None:
        """
        The engine responsible for managing the game
        """

        # HACK: work out how to handle the game session
        for _ in range(1, 1_000_000):

            # get the first question
            problem = self.setup_problem_state()

            response = Interface(self.game_state, self.problem).ask_question()

            # TODO: add translation engine here
            if loose_string_equal(response, problem.solution):
                # user answered correctly
                self.game_state.next_question(problem.problem, problem.solution, True)
                self.game_state.correct_answer()
            else:
                # user is an idiot
                self.game_state.next_question(problem.problem, problem.solution, False)
                self.game_state.incorrect_answer()
