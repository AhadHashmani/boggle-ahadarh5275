import typing
from typing import Optional, Dict

from py_boggle.boggle_dictionary import BoggleDictionary


class TrieNode:
    """
    Our TrieNode class. Feel free to add new properties/functions, but
    DO NOT edit the names of the given properties (children and is_word).
    """
    def __init__(self):
        self.children: Dict[str, "TrieNode"] = {}  # maps a child letter to its TrieNode
        self.is_word = False  # whether or not this Node is a valid word ending


class TrieDictionary(BoggleDictionary):
    """Trie-backed BoggleDictionary. Do NOT rename self.root."""

    def __init__(self):
        self.root: TrieNode = TrieNode()

    def load_dictionary(self, filename: str) -> None:
        with open(filename) as wordsfile:
            for line in wordsfile:
                word = line.strip().lower()
                if not word:
                    continue
                node = self.root
                for ch in word:
                    nxt = node.children.get(ch)
                    if nxt is None:
                        nxt = TrieNode()
                        node.children[ch] = nxt
                    node = nxt
                node.is_word = True

    def traverse(self, prefix: str) -> Optional[TrieNode]:
        """Follow `prefix` down the trie; None if any child is missing."""
        node = self.root
        for ch in prefix.lower():
            node = node.children.get(ch)
            if node is None:
                return None
        return node

    def is_prefix(self, prefix: str) -> bool:
        return self.traverse(prefix) is not None

    def contains(self, word: str) -> bool:
        node = self.traverse(word)
        return node is not None and node.is_word

    def __iter__(self) -> typing.Iterator[str]:
        # Generator: each call gets independent state, raises StopIteration
        # when exhausted, and yields words in lexicographic order.
        def walk(node: TrieNode, prefix: str):
            if node.is_word:
                yield prefix
            for ch in sorted(node.children):
                yield from walk(node.children[ch], prefix + ch)

        return walk(self.root, "")