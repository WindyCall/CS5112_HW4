# Problem 2b - Binary Search with Prefix Sums

def binary_search(packages, boxes):
    def find_max_package_index(sorted_packages, box_size):
        left = 0
        right = len(sorted_packages) - 1
        result = -1

        while left <= right:
            mid = (left + right) // 2

            if sorted_packages[mid] <= box_size:
                result = mid
                left = mid + 1
            else:
                right = mid - 1

        return result

    n = len(packages)

    sorted_packages = sorted(packages)

    prefix_sum = [0] * (n + 1)
    for i in range(n):
        prefix_sum[i + 1] = prefix_sum[i] + sorted_packages[i]

    min_waste = float('inf')

    for supplier_boxes in boxes:
        sorted_boxes = sorted(supplier_boxes)

        if sorted_boxes[-1] < sorted_packages[-1]:
            continue

        total_waste = 0
        prev_count = 0

        for box_size in sorted_boxes:
            max_package_idx = find_max_package_index(sorted_packages, box_size)

            if max_package_idx == -1:
                continue

            num_packages_in_box = max_package_idx + 1 - prev_count

            if num_packages_in_box <= 0:
                continue

            sum_packages = prefix_sum[max_package_idx + 1] - prefix_sum[prev_count]

            total_waste += box_size * num_packages_in_box - sum_packages

            prev_count = max_package_idx + 1

            if prev_count >= n:
                break

        if prev_count >= n:
            min_waste = min(min_waste, total_waste)

    if min_waste == float('inf'):
        return -1

    return min_waste