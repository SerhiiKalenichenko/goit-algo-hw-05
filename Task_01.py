class HashTable:
    def __init__(self, size: int):
        self.size = size
        self.table = [[] for _ in range(self.size)]

    def hash_function(self, key):
        return hash(key) % self.size

    def insert(self, key, value):
        key_hash = self.hash_function(key)
        key_value = [key, value]
        bucket = self.table[key_hash]

        for pair in bucket:
            if pair[0] == key:
                pair[1] = value
                return True

        bucket.append(key_value)
        return True

    def get(self, key):
        key_hash = self.hash_function(key)
        bucket = self.table[key_hash]

        for pair in bucket:
            if pair[0] == key:
                return pair[1]
        return None

    def delete(self, key):
       
        key_hash = self.hash_function(key)
        bucket = self.table[key_hash]

        for index, pair in enumerate(bucket):
            if pair[0] == key:
                bucket.pop(index)
                return True
        return False


if __name__ == "__main__":
    H = HashTable(5)
    H.insert("apple", 10)
    H.insert("orange", 20)
    H.insert("banana", 30)

    print(H.get("apple"))    # 10
    print(H.get("orange"))   # 20
    print(H.get("banana"))   # 30

    H.delete("orange")
    print(H.get("orange"))   # None