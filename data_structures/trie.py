# data_structures/trie.py - Trie for fast location search

class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False
        self.data = None  # Store location data

class Trie:
    """
    Trie for location autocomplete and fast prefix search
    """
    
    def __init__(self):
        self.root = TrieNode()
        self.size_count = 0
    
    def insert(self, word, data=None):
        """Insert a word into trie"""
        word = word.lower()
        node = self.root
        
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        
        if not node.is_end:
            self.size_count += 1
        
        node.is_end = True
        node.data = data
    
    def search(self, word):
        """Check if word exists in trie"""
        word = word.lower()
        node = self.root
        
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        
        return node.is_end
    
    def starts_with(self, prefix):
        """Check if any word starts with prefix"""
        prefix = prefix.lower()
        node = self.root
        
        for char in prefix:
            if char not in node.children:
                return False
            node = node.children[char]
        
        return True
    
    def autocomplete(self, prefix, max_results=10):
        """
        Get all words that start with prefix
        Returns list of (word, data) tuples
        """
        prefix = prefix.lower()
        node = self.root
        
        # Navigate to prefix node
        for char in prefix:
            if char not in node.children:
                return []
            node = node.children[char]
        
        # Collect all words from this node
        results = []
        self._collect_words(node, prefix, results, max_results)
        return results
    
    def _collect_words(self, node, prefix, results, max_results):
        """Helper to collect all words from a node"""
        if len(results) >= max_results:
            return
        
        if node.is_end:
            results.append((prefix, node.data))
        
        for char, child in sorted(node.children.items()):
            self._collect_words(child, prefix + char, results, max_results)
    
    def get_all_words(self):
        """Get all words in trie"""
        results = []
        self._collect_words(self.root, "", results, float('inf'))
        return results
    
    def delete(self, word):
        """Delete a word from trie"""
        word = word.lower()
        
        def _delete(node, word, index):
            if index == len(word):
                if not node.is_end:
                    return False
                node.is_end = False
                node.data = None
                return len(node.children) == 0
            
            char = word[index]
            if char not in node.children:
                return False
            
            should_delete = _delete(node.children[char], word, index + 1)
            
            if should_delete:
                del node.children[char]
                return len(node.children) == 0 and not node.is_end
            
            return False
        
        if _delete(self.root, word, 0):
            self.size_count -= 1
    
    def size(self):
        """Get number of words in trie"""
        return self.size_count
    
    def clear(self):
        """Clear all words"""
        self.root = TrieNode()
        self.size_count = 0