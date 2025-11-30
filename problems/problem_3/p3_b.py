# Problem 3 - Count-Min Sketch

def count_min_sketch(a, b, p, w, stream):
    """
    Implement Count-Min Sketch (CMS) data structure.

    The CMS uses multiple hash functions to count elements in a stream.
    Each row uses a hash function: h_i(x) = ((a_i * x + b_i) % p) % w

    Inputs:
    - a, b: vectors with positive entries (hash function parameters)
    - p, w: scalars (p is modulus, w is width of sketch)
    - stream: Python generator/iterator that produces stream of data elements

    Outputs:
    - A sketch matrix of size d x w, where d = len(a)
      sketch[i][j] = count of elements that hash to position j in row i
    """
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


# Test with the example from the problem description
if __name__ == "__main__":
    # Example: d=2, w=3, a=[1,2], b=[3,5], p=100
    # Stream: [10, 11, 10]
    # Expected output: [[0, 2, 1], [1, 2, 0]]

    print("Test 1 (from problem description):")
    result = count_min_sketch(
        a=[1, 2],
        b=[3, 5],
        p=100,
        w=3,
        stream=iter([10, 11, 10])
    )
    print(f"Result: {result}")
    print(f"Expected: [[0, 2, 1], [1, 2, 0]]")
    print(f"Match: {result == [[0, 2, 1], [1, 2, 0]]}")

    # Let's verify the hash computations manually:
    print("\nManual verification:")
    print("For element 10:")
    print(f"  h_1(10) = ((1*10 + 3) % 100) % 3 = (13 % 100) % 3 = 13 % 3 = 1")
    print(f"  h_2(10) = ((2*10 + 5) % 100) % 3 = (25 % 100) % 3 = 25 % 3 = 1")

    print("For element 11:")
    print(f"  h_1(11) = ((1*11 + 3) % 100) % 3 = (14 % 100) % 3 = 14 % 3 = 2")
    print(f"  h_2(11) = ((2*11 + 5) % 100) % 3 = (27 % 100) % 3 = 27 % 3 = 0")

    print("For element 10 (again):")
    print(f"  h_1(10) = 1, h_2(10) = 1")

    print("\nRow 0: position 1 gets count 2, position 2 gets count 1 → [0, 2, 1]")
    print("Row 1: position 0 gets count 1, position 1 gets count 2 → [1, 2, 0]")

    # Test 2
    print("\n" + "="*60)
    print("Test 2:")
    result2 = count_min_sketch(
        a=[2, 3, 2, 5],
        b=[1, 10, 200, 4],
        p=9,
        w=4,
        stream=iter([129, 56, 117, 142, 82, 161, 114, 68, 161, 149])
    )
    print(f"Result: {result2}")
    print(f"Expected: [[3, 2, 3, 2], [2, 3, 0, 5], [4, 1, 2, 3], [4, 2, 2, 2]]")
    print(f"Match: {result2 == [[3, 2, 3, 2], [2, 3, 0, 5], [4, 1, 2, 3], [4, 2, 2, 2]]}")
