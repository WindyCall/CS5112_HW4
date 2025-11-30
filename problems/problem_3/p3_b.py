# Problem 3 - Count-Min Sketch

def count_min_sketch(a, b, p, w, stream):
    d = len(a)  # Number of rows (number of hash functions)

    # Initialize the sketch matrix with zeros
    sketch = [[0] * w for _ in range(d)]

    # Process each element in the stream
    for element in stream:
        # For each hash function (row)
        for i in range(d):
            # Compute hash: h_i(x) = ((a_i * x + b_i) % p) % w
            hash_value = ((a[i] * element + b[i]) % p) % w

            # Increment the count at the hashed position
            sketch[i][hash_value] += 1

    return sketch