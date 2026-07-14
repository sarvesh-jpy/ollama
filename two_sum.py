def two_sum(nums, target):
    """
    Returns the indices of the two numbers that add up to the target.

    Parameters:
    nums (List[int]): List of integers.
    target (int): The target sum.

    Returns:
    List[int]: Indices of the two numbers that add to the target.

    Time Complexity: O(n) - Single pass through the list.
    Space Complexity: O(n) - Hash map storage.

    Example:
    >>> two_sum([2,7,11,15], 9)
    [0, 1]
    """
    num_to_index = {}
    for index, num in enumerate(nums):
        complement = target - num
        if complement in num_to_index:
            return [num_to_index[complement], index]
        num_to_index[num] = index
    # The problem assumes there is exactly one solution, so no need for error handling.

# Example usage
if __name__ == "__main__":
    nums = [2, 7, 11, 15]
    target = 9
    print(two_sum(nums, target))  # Output: [0, 1]
