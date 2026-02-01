# data_structures/segment_tree.py - Segment Tree for Range Queries

class SegmentTree:
    """
    Segment Tree for efficient range queries
    Used for analyzing emergency counts in time ranges
    """
    
    def __init__(self, data):
        """Initialize with array of data"""
        self.n = len(data)
        self.tree = [0] * (4 * self.n)
        if data:
            self._build(data, 0, 0, self.n - 1)
    
    def _build(self, data, node, start, end):
        """Build segment tree recursively"""
        if start == end:
            self.tree[node] = data[start]
            return
        
        mid = (start + end) // 2
        left_child = 2 * node + 1
        right_child = 2 * node + 2
        
        self._build(data, left_child, start, mid)
        self._build(data, right_child, mid + 1, end)
        
        self.tree[node] = self.tree[left_child] + self.tree[right_child]
    
    def update(self, index, value):
        """Update value at index"""
        self._update(0, 0, self.n - 1, index, value)
    
    def _update(self, node, start, end, index, value):
        """Update helper"""
        if start == end:
            self.tree[node] = value
            return
        
        mid = (start + end) // 2
        left_child = 2 * node + 1
        right_child = 2 * node + 2
        
        if index <= mid:
            self._update(left_child, start, mid, index, value)
        else:
            self._update(right_child, mid + 1, end, index, value)
        
        self.tree[node] = self.tree[left_child] + self.tree[right_child]
    
    def query(self, left, right):
        """Query sum in range [left, right]"""
        if left > right or left < 0 or right >= self.n:
            return 0
        return self._query(0, 0, self.n - 1, left, right)
    
    def _query(self, node, start, end, left, right):
        """Query helper"""
        # No overlap
        if right < start or left > end:
            return 0
        
        # Complete overlap
        if left <= start and end <= right:
            return self.tree[node]
        
        # Partial overlap
        mid = (start + end) // 2
        left_child = 2 * node + 1
        right_child = 2 * node + 2
        
        left_sum = self._query(left_child, start, mid, left, right)
        right_sum = self._query(right_child, mid + 1, end, left, right)
        
        return left_sum + right_sum
    
    def range_max(self, left, right):
        """Find maximum in range [left, right]"""
        if left > right or left < 0 or right >= self.n:
            return float('-inf')
        return self._range_max(0, 0, self.n - 1, left, right)
    
    def _range_max(self, node, start, end, left, right):
        """Range max helper"""
        if right < start or left > end:
            return float('-inf')
        
        if left <= start and end <= right:
            return self.tree[node]
        
        mid = (start + end) // 2
        left_child = 2 * node + 1
        right_child = 2 * node + 2
        
        left_max = self._range_max(left_child, start, mid, left, right)
        right_max = self._range_max(right_child, mid + 1, end, left, right)
        
        return max(left_max, right_max)