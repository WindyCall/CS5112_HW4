# Problem 2b - Binary Search with Prefix Sums

def binary_search(packages, boxes):
    def find_max_package_index(sorted_packages, box_size):
        """
        Find the index of the largest package that can fit in the box using binary search.

        Args:
            sorted_packages: Sorted list of package sizes
            box_size: Size of the box

        Returns:
            int: Index of largest package that fits, or -1 if no package fits
        """
        left = 0
        right = len(sorted_packages) - 1
        result = -1

        while left <= right:
            mid = (left + right) // 2

            if sorted_packages[mid] <= box_size:
                # This package fits, try to find a larger one
                result = mid
                left = mid + 1
            else:
                # This package is too large, search left half
                right = mid - 1

        return result

    n = len(packages)

    # Sort packages once for all suppliers
    sorted_packages = sorted(packages)

    # Compute prefix sum of sorted packages for O(1) range sum queries
    # prefix_sum[i] = sum of packages[0..i-1]
    prefix_sum = [0] * (n + 1)
    for i in range(n):
        prefix_sum[i + 1] = prefix_sum[i] + sorted_packages[i]

    min_waste = float('inf')

    # Try each supplier
    for supplier_boxes in boxes:
        # Sort this supplier's boxes
        sorted_boxes = sorted(supplier_boxes)

        # Check if largest box can fit largest package
        if sorted_boxes[-1] < sorted_packages[-1]:
            # This supplier cannot fit all packages
            continue

        # Calculate total waste for this supplier using prefix sums
        total_waste = 0
        prev_count = 0  # Number of packages already assigned to previous boxes

        # For each box (in sorted order)
        for box_size in sorted_boxes:
            # Binary search: find the index of the largest package that fits in this box
            max_package_idx = find_max_package_index(sorted_packages, box_size)

            if max_package_idx == -1:
                # This box is too small for even the smallest package
                continue

            # Number of packages that fit in this box (that haven't been assigned yet)
            num_packages_in_box = max_package_idx + 1 - prev_count

            if num_packages_in_box <= 0:
                # All packages that fit in this box were already assigned to smaller boxes
                continue

            # Sum of package sizes from prev_count to max_package_idx (inclusive)
            sum_packages = prefix_sum[max_package_idx + 1] - prefix_sum[prev_count]

            # Waste = (box_size * count) - sum_of_packages
            total_waste += box_size * num_packages_in_box - sum_packages

            # Update prev_count
            prev_count = max_package_idx + 1

            # If we've assigned all packages, we're done
            if prev_count >= n:
                break

        # Check if all packages were assigned
        if prev_count >= n:
            min_waste = min(min_waste, total_waste)

    # Return -1 if no supplier can fit all packages
    if min_waste == float('inf'):
        return -1

    return min_waste