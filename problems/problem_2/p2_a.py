# Problem 2 a

def linear_search(packages, boxes):
  sorted_packages = sorted(packages)

  min_waste = float('inf')

  for supplier_boxes in boxes:
    sorted_boxes = sorted(supplier_boxes)

    total_waste = 0
    can_fit_all = True

    for package in sorted_packages:
      best_box = None
      for box in sorted_boxes:
        if box >= package:
          if best_box is None or box < best_box:
            best_box = box

      if best_box is None:
        can_fit_all = False
        break

      total_waste += best_box - package

    if can_fit_all:
      min_waste = min(min_waste, total_waste)

  if min_waste == float('inf'):
    return -1

  return min_waste