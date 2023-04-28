from abc import ABC, abstractmethod


class AbstractParaphraser(ABC):

    @abstractmethod
    def extract_noun_phrases(self, tree):
        pass

    @abstractmethod
    def generate_np_permutations(self, np_lists):
        pass

    @abstractmethod
    def replace_nps(self, tree, np_permutations):
        pass

    @abstractmethod
    def generate_paraphrases(self):
        pass
