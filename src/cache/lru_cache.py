from collections import OrderedDict


class LRUCache:
    def __init__(self, capacity=10):
        self.cache = OrderedDict()
        self.capacity = capacity

    def _hash_function(self, key):
        hash_value = 31
        for char in key:
            hash_value = ((hash_value << 5) + hash_value) + ord(char)
        return hash_value % self.capacity


    def get(self, key):
        if key not in self.cache:
            print("CACHE MISS!!!")
            return -1

        self.cache.move_to_end(key)

        print(f"Cached data -> Key: {key} Value: {self.cache[key]}")
        return self.cache[key]

    def put(self, value):
        key = self._hash_function(value)

        if key in self.cache:
            print("CACHE COLLISION!!!")
            print(f"Replacing: {self.cache[key]} by {value}")
            self.cache.move_to_end(key)

        self.cache[key] = value

        if len(self.cache) > self.capacity:
            print("CACHE CAPACITY REACHED!!!")
            print("Popping LRU item")
            self.cache.popitem(last=False)

        print(f"Data cached successfully!")
        return key



# Instantiate LRU Cache
lru_cache =LRUCache()

words = [
    "apple", "banana", "cherry", "date", "elephant",
    "fig", "grape", "honeydew", "iceberg", "jackfruit",
    "kiwi", "lemon", "mango", "nectarine", "orange",
    "papaya", "quince", "raspberry", "strawberry", "tomato",
    "ugly", "vanilla", "watermelon", "xmas", "yam", "zucchini"
]

for word in words:
    # put
    print("\nPut data to Cache")

    lru_cache.put(word)
    print(f"\nCache: {sorted(dict(lru_cache.cache).items())} | Length : {len(lru_cache.cache)}")


# get
print("\nGet Cached data")
lru_cache.get(key=0)
lru_cache.get(key=1)
lru_cache.get(key=2)
lru_cache.get(key=3)
lru_cache.get(key=4)
lru_cache.get(key=5)
lru_cache.get(key=6)
lru_cache.get(key=7)
lru_cache.get(key=8)
lru_cache.get(key=9)
