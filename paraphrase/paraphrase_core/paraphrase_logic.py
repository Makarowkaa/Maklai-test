import nltk
import itertools
from paraphrase.paraphrase_core.abstract_paraphrase import AbstractParaphraser


class Paraphraser(AbstractParaphraser):
    """
    A class for generating paraphrases from a tree.

    Attributes:
        tree: The tree to generate paraphrases from.
        limit: The maximum number of paraphrases to generate, defaults to 20.

    Methods:
        extract_noun_phrases: Extracts noun phrases from the tree.
        generate_np_permutations: Generates all possible permutations for the extracted noun phrases.
        replace_nps: Replaces the original noun phrases in the tree with the permutations.
        generate_paraphrases: Generates paraphrases from the tree.
    """
    def __init__(self, tree_string, limit=20):
        self.tree = nltk.Tree.fromstring(tree_string)
        self.limit = limit

    def extract_noun_phrases(self, tree):
        """
        Extracts noun phrases from the tree.

        Params:
            tree: The tree to extract noun phrases from.

        Returns:
             A list of two lists of noun phrases separated by commas or conjunctions.
        """
        np_lists = []

        def traverse_tree(node, inside_np=False):
            """
            Recursively traverses the tree to find noun phrases.

            Args:
                node: The node in the tree to traverse.
                inside_np: Whether the current node is inside a noun phrase.
            """
            if isinstance(node, nltk.Tree):
                if node.label() == 'NP':
                    children_labels = [child.label() for child in node]

                    # Check if the NP contains a comma or conjunction
                    if any(label in children_labels for label in {',', 'CC'}):
                        # Extract NPs inside the current NP
                        extracted_nps = [child for child in node if child.label() == 'NP']

                        # Add a new list to np_lists if not inside an NP
                        if not inside_np:
                            np_lists.append([])

                        # Add the extracted NPs to the last list in np_lists
                        np_lists[-1].extend(extracted_nps)
                        inside_np = True
                    else:
                        inside_np = False

                    # Continue traversal for each child
                    for child in node:
                        traverse_tree(child, inside_np)
                else:
                    inside_np = False
                    for child in node:
                        traverse_tree(child, inside_np)

        # Call the traversal function starting from the root of the tree
        traverse_tree(tree)

        # Convert the extracted NPs to strings and return them
        return [[str(np) for np in np_list] for np_list in np_lists]

    def generate_np_permutations(self, np_lists):
        """
        Generates all possible permutations for the extracted noun phrases.

        Args:
            np_lists: A list of two lists of noun phrases separated by commas or conjunctions.

        Returns:
            A list of two lists of permutations for the extracted noun phrases.
        """
        permutations = []

        # Iterate through the lists of noun phrases
        for np_list in np_lists:
            # Generate all permutations for the current list
            perms = list(itertools.permutations(np_list))
            # Add the permutations to the result
            permutations.append(perms)

        return permutations

    def replace_nps(self, tree, np_permutations):
        """
        Replaces the original noun phrases in the tree with the permutations.

        Args:
            tree: The tree to replace noun phrases in.
            np_permutations: A list of two lists of permutations for the extracted noun phrases.

        Returns:
            The tree with the noun phrases replaced.
        """
        # Create a deep copy of the input tree
        replaced_tree = tree.copy(deep=True)

        def traverse_tree(node, np_list_index=0):
            """
            Recursively traverses the tree to replace noun phrases.

            Args:
                node: The node in the tree to traverse.
                np_list_index: The index of the current noun phrase permutation.
            """
            nonlocal np_permutations

            if isinstance(node, nltk.Tree):
                if node.label() == 'NP':
                    children_labels = [child.label() for child in node]

                    # Check if the NP contains a comma or conjunction
                    if any(label in children_labels for label in {',', 'CC'}):
                        # Get the replacement NP from the current permutation
                        np_replacement = np_permutations[np_list_index]
                        # Create a copy of the replacement NPs
                        np_replacement_copy = list(np_replacement)
                        # Replace the original NPs with the new ones
                        for i, child in enumerate(node):
                            if child.label() == 'NP':
                                node[i] = np_replacement_copy.pop(0)
                        # Increment the np_list_index
                        np_list_index += 1

                    # Continue traversal for each child
                    for child in node:
                        np_list_index = traverse_tree(child, np_list_index)
                else:
                    for child in node:
                        np_list_index = traverse_tree(child, np_list_index)

            return np_list_index

        # Call the traversal function starting from the root of the replaced_tree
        traverse_tree(replaced_tree)
        return replaced_tree

    def generate_paraphrases(self):
        """
        Generates paraphrases from the input tree string.

        Returns:
            A dictionary containing a list of paraphrase trees.
        """
        # Get the input tree
        tree = self.tree
        # Extract NPs from the tree
        np_lists = self.extract_noun_phrases(tree)
        # Generate permutations for the extracted NPs
        permutations = self.generate_np_permutations(np_lists)
        # Initialize a list to store paraphrase strings
        paraphrase_strs = []

        # Iterate over the product of permutations, limited by the "limit" parameter
        for np_permutation in itertools.islice(itertools.product(*permutations), self.limit):
            # Replace the original NPs with the new permutations in the tree
            paraphrase = self.replace_nps(tree, np_permutation)
            # Convert the paraphrase tree to a string and add it to the list
            paraphrase_strs.append(paraphrase.pformat(margin=float("inf")))

        # Return a dictionary containing a list of paraphrase trees
        return {"paraphrases": [{"tree": paraphrase} for paraphrase in paraphrase_strs]}
