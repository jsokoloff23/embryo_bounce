import ast
import configparser
import os

from utils import constants

class HighScoreManager(configparser.ConfigParser):
    SECTION = "High Scores"
    OPTION = "highscores"
    NUM_PLAYERS = 5
    def __init__(self):
        super().__init__()
        self.filename = constants.HS_CFG_PATH
        self.entries: list = []
        self._init_from_file()

    def get_entries(self):
        section = HighScoreManager.SECTION
        option = HighScoreManager.OPTION
        if self.has_section(section):
            return ast.literal_eval(self.get(section, option))
        else:
            return []
        
    def is_high_score(self, new_score):
        scores = self._get_scores()
        if len(self.entries) < HighScoreManager.NUM_PLAYERS:
            return True
        for score in scores:
            if new_score > score:
                return True
        return False

    def write_new_high_score(self, new_name: str, new_score: int):
        if not self.has_section(HighScoreManager.SECTION):
            self.add_section(HighScoreManager.SECTION)
        num_players = HighScoreManager.NUM_PLAYERS
        is_high_score = self.is_high_score(new_score)
        value = (new_name, new_score)
        if self.entries:
            if is_high_score:
                index = self._get_new_index(new_score)
                if index == num_players - 1:
                    self.entries[index] = value
                elif index is not None:
                    self.entries.insert(index, value)
                    if len(self.entries) > num_players:
                        del self.entries[-1]
                else:
                    self.entries.append(value)
        else:
            self.entries.append(value)
        self._write_entries()

    def _get_new_index(self, new_score):
        scores = self._get_scores()
        for index, score in enumerate(scores):
            if new_score > score:
                return index

    def _get_scores(self):
        return [int(entry[1]) for entry in self.entries]

    def _init_from_file(self):
        """
        Initializes Config from file located at file_path. 
        """
        if os.path.exists(self.filename):
            self.read(self.filename)
            self.entries = self.get_entries()
    
    def _write_entries(self):
        section = HighScoreManager.SECTION
        option = HighScoreManager.OPTION
        self.set(section, option, str(self.entries))
        with open(self.filename, "w") as configfile:
            self.write(configfile)
