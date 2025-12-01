# Problem 3 - Count-Min Sketch

def count_min_sketch(a, b, p, w, stream):
    d = len(a)

    sketch = [[0] * w for _ in range(d)]

    for element in stream:
        for i in range(d):
            hash_value = ((a[i] * element + b[i]) % p) % w

            sketch[i][hash_value] += 1

    return sketch