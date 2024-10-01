import os


class Interface:
    """
    used to try make a better interface for this
    """

    def __init__(self, game_state, problem_state):

        self.game_state = game_state
        self.problem_state = problem_state

    def onek_question(self):

        question = "\tWould you like the 1k words version? (y/n): "

        return self.response_manager(question)

    def ask_question(self):

        response = self.response_manager("\tTranslate: ")

        return response

    def incorrect_answer(self):

        # Wrong answer message
        failed_string = f"""
    Wrong:
        {self.content['last_target']}
    Should translate to:
        {self.content['last_answer']}
        """

        return failed_string

    def correct_answer(self):

        success_string = f"""
    CORRECT!
        {self.game_state.last_target} is {self.game_state.last_answer}
        """

        return success_string

    def response_manager(self, custom_question=None):

        os.system("cls" if os.name == "nt" else "clear")

        # first print
        if not self.problem_state.problem:
            output = """
        =================================
        CWS - Translation Game - Spanish
        ==================================
        """
        # second print
        elif self.problem_state.problem and not self.game_state.last_translation:
            output = f"""
        =================================
        CWS - Translation Game - Spanish
        ==================================
            Streak: {self.game_state.streak} High Score: {self.game_state.high_score} Miss Streak: {self.game_state.low_score} Lex size: {self.problem_state.set_size}
        ==================================

            Translate: {self.problem_state.problem}
        """
        # nth passing
        elif (
            self.problem_state.problem
            and self.game_state.last_translation
            and self.game_state.previous_correct
        ):
            output = f"""
        =================================
        CWS - Translation Game - Spanish
        ==================================
            Streak: {self.game_state.streak} High Score: {self.game_state.high_score} Miss Streak: {self.game_state.low_score} Lex size: {self.problem_state.set_size}
        ==================================

            Correct: {self.game_state.last_translation} is {self.game_state.last_answer}

            Translate: {self.problem_state.problem}
        """
        # nth failing
        elif (
            self.problem_state.problem
            and self.game_state.last_translation
            and not self.game_state.previous_correct
        ):
            output = f"""
        =================================
        CWS - Translation Game - Spanish
        ==================================
            Streak: {self.game_state.streak} High Score: {self.game_state.high_score} Miss Streak: {self.game_state.low_score} Lex size: {self.problem_state.set_size}
        ==================================

            Incorrect: {self.game_state.last_translation} is {self.game_state.last_answer}

            Reverso Contexto: https://context.reverso.net/translation/spanish-english/{self.game_state.last_translation}

            Translate: {self.problem_state.problem}
        """

        print(output)

        if custom_question:
            guess = input(f"{custom_question}")

            return guess
