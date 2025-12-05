from typing import List, Tuple, Optional

def binary_search_with_upper_bound(arr: List[float], target: float) -> Tuple[int, Optional[float]]:
    
    left, right = 0, len(arr) - 1
    iterations = 0
    upper_bound: Optional[float] = None

    while left <= right:
        iterations += 1
        mid = (left + right) // 2
        mid_val = arr[mid]

        if mid_val >= target:
            upper_bound = mid_val
            right = mid - 1
        else:
            left = mid + 1

    return iterations, upper_bound

if __name__ == "__main__":
    data = [0.5, 1.2, 2.7, 3.3, 4.8, 5.0]

    print(binary_search_with_upper_bound(data, 2.0))  # (ітерації, 2.7)
    print(binary_search_with_upper_bound(data, 3.3))  # (ітерації, 3.3)
    print(binary_search_with_upper_bound(data, 6.0))  # (ітерації, None)