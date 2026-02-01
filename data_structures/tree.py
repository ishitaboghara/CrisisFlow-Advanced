# data_structures/tree.py - Binary Search Tree

class TreeNode:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.left = None
        self.right = None
        self.height = 1

class BST:
    """
    Binary Search Tree for storing resolved emergencies
    Key: emergency type, Value: emergency data
    """
    
    def __init__(self):
        self.root = None
        self.size_count = 0
    
    def insert(self, key, value):
        """Insert a key-value pair"""
        self.root = self._insert(self.root, key, value)
        self.size_count += 1
    
    def _insert(self, node, key, value):
        if node is None:
            return TreeNode(key, value)
        
        if key < node.key:
            node.left = self._insert(node.left, key, value)
        else:
            node.right = self._insert(node.right, key, value)
        
        return node
    
    def search(self, key):
        """Search for all values with given key"""
        results = []
        self._search(self.root, key, results)
        return results
    
    def _search(self, node, key, results):
        if node is None:
            return
        
        if key < node.key:
            self._search(node.left, key, results)
        elif key > node.key:
            self._search(node.right, key, results)
        else:
            results.append(node.value)
            # Check both sides as duplicates allowed
            self._search(node.left, key, results)
            self._search(node.right, key, results)
    
    def inorder(self):
        """Inorder traversal (sorted order)"""
        result = []
        self._inorder(self.root, result)
        return result
    
    def _inorder(self, node, result):
        if node:
            self._inorder(node.left, result)
            result.append(node.value)
            self._inorder(node.right, result)
    
    def preorder(self):
        """Preorder traversal"""
        result = []
        self._preorder(self.root, result)
        return result
    
    def _preorder(self, node, result):
        if node:
            result.append(node.value)
            self._preorder(node.left, result)
            self._preorder(node.right, result)
    
    def postorder(self):
        """Postorder traversal"""
        result = []
        self._postorder(self.root, result)
        return result
    
    def _postorder(self, node, result):
        if node:
            self._postorder(node.left, result)
            self._postorder(node.right, result)
            result.append(node.value)
    
    def get_height(self):
        """Get height of tree"""
        return self._get_height(self.root)
    
    def _get_height(self, node):
        if node is None:
            return 0
        return 1 + max(self._get_height(node.left), self._get_height(node.right))
    
    def get_all_keys(self):
        """Get all unique keys"""
        keys = set()
        self._get_keys(self.root, keys)
        return sorted(keys)
    
    def _get_keys(self, node, keys):
        if node:
            keys.add(node.key)
            self._get_keys(node.left, keys)
            self._get_keys(node.right, keys)
    
    def count_by_key(self):
        """Count occurrences of each key"""
        counts = {}
        for item in self.inorder():
            key = item.get("type", "Unknown")
            counts[key] = counts.get(key, 0) + 1
        return counts
    
    def size(self):
        """Get total number of nodes"""
        return self.size_count
    
    def is_empty(self):
        """Check if tree is empty"""
        return self.root is None