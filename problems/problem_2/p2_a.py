# Problem 2 a

def linear_search(packages, boxes):
  # Sort packages once for all suppliers
  sorted_packages = sorted(packages)

  min_waste = float('inf')

  # Try each supplier
  for supplier_boxes in boxes:
    # Sort this supplier's boxes
    sorted_boxes = sorted(supplier_boxes)

    # Check if this supplier can fit all packages
    total_waste = 0
    can_fit_all = True

    # For each package, find the smallest box that can fit it using linear search
    for package in sorted_packages:
      # Linear search: go through all boxes to find smallest that fits
      best_box = None
      for box in sorted_boxes:
        if box >= package:
          if best_box is None or box < best_box:
            best_box = box

      # If no box can fit this package, this supplier won't work
      if best_box is None:
        can_fit_all = False
        break

      total_waste += best_box - package

    # If this supplier can fit all packages, update minimum waste
    if can_fit_all:
      min_waste = min(min_waste, total_waste)

  # Return -1 if no supplier can fit all packages
  if min_waste == float('inf'):
    return -1

  return min_waste