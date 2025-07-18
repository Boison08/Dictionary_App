#The above code is a Python implementation of a dictionary using a Binary Search Tree (BST) data structure. 
# The dictionary allows users to insert new words with meanings and example sentences, search for words, delete words, and get the word of the day. 
# The dictionary data is stored in a JSON file for persistence across sessions.
#The code should be executed from gui_dictionary.py file to see the output.

#Names of group members
# 1. Clement Yeboah Adjapong
# 2. Brian Okyere Akosah
# 3. Simeon Anyinmyamfo Awotwe Boison
# 4. Kwesi Odartey Dadzie
# 5. Salma Niina Ibrahim
# 6. Kobina Ansu Adjei Kyeremeh
# 7. Ahmed Mohammed
# 8. Adam Musah Wandaogo



import json
import random
import datetime

class Node:
    """A node in the Binary Search Tree representing a dictionary entry"""
    def __init__(self, word, meaning, example_sentence=""):
        self.word = word.lower()  # Store word in lowercase for case-insensitive comparison
        self.meaning = meaning
        self.example_sentence = example_sentence
        self.left = None  # Left child pointer
        self.right = None  # Right child pointer

class BSTDictionary:
    """Binary Search Tree implementation of a dictionary"""
    def __init__(self):
        self.root = None  # Root node of the BST
        self.recent_searches = []  # List to track recent word lookups
        self.load_from_file()  # Load existing dictionary data
        self.word_of_the_day = self.get_word_of_the_day()  # Initialize word of the day

    def insert(self, word, meaning, example_sentence=""):
        """Public method to insert a new word into the dictionary"""
        self.root = self._insert_recursive(self.root, word, meaning, example_sentence)
        self.save_to_file()  # Save changes to file after insertion

    def _insert_recursive(self, node, word, meaning, example_sentence):
        """Helper method for recursive insertion of words"""
        if node is None:
            return Node(word, meaning, example_sentence)
        if word.lower() < node.word:
            node.left = self._insert_recursive(node.left, word, meaning, example_sentence)
        elif word.lower() > node.word:
            node.right = self._insert_recursive(node.right, word, meaning, example_sentence)
        else:
            # Update existing word's meaning and example
            node.meaning = meaning
            node.example_sentence = example_sentence
        return node

    def search(self, word):
        """Public method to search for a word in the dictionary"""
        result = self._search_recursive(self.root, word.lower())
        if result:
            self.recent_searches.append(word.lower())  # Track successful searches
        return result

    def _search_recursive(self, node, word):
        """Helper method for recursive word search"""
        if node is None:
            return None
        if word == node.word:
            return node
        elif word < node.word:
            return self._search_recursive(node.left, word)
        else:
            return self._search_recursive(node.right, word)

    def load_from_file(self, filename="dictionary.json"):
        """Load dictionary data from a JSON file"""
        try:
            with open(filename, "r") as file:
                content = file.read().strip()
                if content:
                    words = json.loads(content)
                    for word, data in words.items():
                        self.insert(word, data["meaning"], data.get("example", ""))
        except FileNotFoundError:
            print("No dictionary file found. Starting fresh.")
        except json.JSONDecodeError:
            print("Error decoding dictionary file. Starting fresh.")

    def save_to_file(self, filename="dictionary.json"):
        """Save dictionary data to a JSON file"""
        words = {}
        self._save_recursive(self.root, words)
        try:
            with open(filename, "w") as file:
                json.dump(words, file, indent=4)
            print("Dictionary saved successfully.")
        except Exception as e:
            print(f"Error saving dictionary: {e}")

    def _save_recursive(self, node, words):
        """Helper method for recursive saving of dictionary data"""
        if node:
            self._save_recursive(node.left, words)
            words[node.word] = {
                "meaning": node.meaning,
                "example": node.example_sentence
            }
            self._save_recursive(node.right, words)

    def get_word_of_the_day(self):
        """Select a random word that changes daily using date as seed"""
        words = self.inorder_traversal()
        if words:
            # Use today's date as seed for consistent daily word
            random.seed(datetime.date.today().toordinal())
            return random.choice(words)
        return None

    def inorder_traversal(self):
        """Public method for inorder traversal of the BST"""
        words = []
        self._inorder_recursive(self.root, words)
        return words

    def _inorder_recursive(self, node, words):
        """Helper method for recursive inorder traversal"""
        if node:
            self._inorder_recursive(node.left, words)
            words.append((node.word, node.meaning, node.example_sentence))
            self._inorder_recursive(node.right, words)

    def delete(self, word):
        """Public method to delete a word from the dictionary"""
        self.root = self._delete_recursive(self.root, word.lower())
        self.save_to_file()  # Save changes after deletion

    def _delete_recursive(self, node, word):
        """Helper method for recursive deletion of words"""
        if node is None:
            return None
        if word < node.word:
            node.left = self._delete_recursive(node.left, word)
        elif word > node.word:
            node.right = self._delete_recursive(node.right, word)
        else:
            # Node with only one child or no child
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left
            # Node with two children
            min_larger_node = self._find_min(node.right)
            node.word = min_larger_node.word
            node.meaning = min_larger_node.meaning
            node.example_sentence = min_larger_node.example_sentence
            node.right = self._delete_recursive(node.right, min_larger_node.word)
        return node

    def _find_min(self, node):
        """Helper method to find the minimum value node in a subtree"""
        current = node
        while current.left is not None:
            current = current.left
        return current