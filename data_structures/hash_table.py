# data_structures/hash_table.py - Hash Table with chaining

class HashTable:
    """
    Hash table for fast emergency lookup by location or ID
    Uses separate chaining for collision resolution
    """
    
    def __init__(self, size=100):
        self.size = size
        self.table = [[] for _ in range(size)]
        self.count = 0
    
    def _hash(self, key):
        """Hash function using polynomial rolling"""
        hash_value = 0
        for i, char in enumerate(str(key)):
            hash_value += ord(char) * (31 ** i)
        return hash_value % self.size
    
    def insert(self, key, value):
        """Insert key-value pair"""
        index = self._hash(key)
        bucket = self.table[index]
        
        # Update if key exists
        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)
                return
        
        # Insert new
        bucket.append((key, value))
        self.count += 1
        
        # Rehash if load factor > 0.7
        if self.count / self.size > 0.7:
            self._rehash()
    
    def get(self, key):
        """Get value by key"""
        index = self._hash(key)
        bucket = self.table[index]
        
        for k, v in bucket:
            if k == key:
                return v
        
        return None
    
    def get_all(self, key):
        """Get all values for a key (if multiple exist)"""
        index = self._hash(key)
        bucket = self.table[index]
        
        return [v for k, v in bucket if k == key]
    
    def delete(self, key):
        """Delete key-value pair"""
        index = self._hash(key)
        bucket = self.table[index]
        
        for i, (k, v) in enumerate(bucket):
            if k == key:
                del bucket[i]
                self.count -= 1
                return v
        
        return None
    
    def contains(self, key):
        """Check if key exists"""
        index = self._hash(key)
        bucket = self.table[index]
        
        return any(k == key for k, v in bucket)
    
    def keys(self):
        """Get all keys"""
        keys = []
        for bucket in self.table:
            keys.extend([k for k, v in bucket])
        return keys
    
    def values(self):
        """Get all values"""
        values = []
        for bucket in self.table:
            values.extend([v for k, v in bucket])
        return values
    
    def items(self):
        """Get all key-value pairs"""
        items = []
        for bucket in self.table:
            items.extend(bucket)
        return items
    
    def _rehash(self):
        """Rehash when load factor too high"""
        old_table = self.table
        self.size *= 2
        self.table = [[] for _ in range(self.size)]
        self.count = 0
        
        for bucket in old_table:
            for key, value in bucket:
                self.insert(key, value)
    
    def get_stats(self):
        """Get hash table statistics"""
        non_empty = sum(1 for bucket in self.table if bucket)
        max_chain = max(len(bucket) for bucket in self.table)
        avg_chain = self.count / non_empty if non_empty > 0 else 0
        
        return {
            "size": self.size,
            "count": self.count,
            "load_factor": self.count / self.size,
            "non_empty_buckets": non_empty,
            "max_chain_length": max_chain,
            "avg_chain_length": avg_chain
        }
    
    def clear(self):
        """Clear all entries"""
        self.table = [[] for _ in range(self.size)]
        self.count = 0