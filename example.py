import numpy as np


def euclidian_distance(vec_a: np.ndarray, vec_b: np.ndarray, axis: int) -> np.ndarray:
    """Calculate distance between two vectors.

    Args:
        vec_a (np.ndarray): N-dimensional vector A
        vec_b (np.ndarray): N-dimensional vector B
        axis (int): Axis to calculate the distance.
                    Useful when comparing multiple vectors.

    Returns:
        np.ndarray: Array with the distance between the vectors.

    Example:
        >>> vec_a = np.array([[1, 2, 3], [4, 5, 6]])
        >>> vec_b = np.array([[7, 8, 9], [10, 11, 12]])
        >>> euclidian_distance(vec_a, vec_b, axis=1)
        array([10.39230485, 10.39230485])
        >>> euclidian_distance(vec_a, vec_b, axis=0)
        array([10.39230485])
    """
    distance = np.linalg.norm(vec_a - vec_b, axis=axis)
    if axis == 0:
        distance = np.array([distance], dtype=vec_a.dtype)
    return distance


def mean_euclidian_distance(vec_a: np.ndarray, vec_b: np.ndarray) -> float:
    """Mean Euclidian distance between two vectors.

    Args:
        vec_a (np.ndarray): 2-dimensional vector A (N, M)
        vec_b (np.ndarray): 2-dimensional vector B (N, M)

    Raises:
        ValueError: If input vectors have:
            - No values
            - Different shapes
            - Different data types

    Returns:
        float: Mean Euclidian distance between the vectors.
    """
    if not vec_a.size or not vec_b.size:
        raise ValueError("Input vectors must have at least one value")
    if vec_a.shape != vec_b.shape:
        raise ValueError("Input vectors must have the same shape")
    if vec_a.dtype != vec_b.dtype:
        raise TypeError("Input vectors must have the same data type")

    distances = euclidian_distance(vec_a, vec_b, axis=1)
    return np.mean(distances)


# FIXME: This function is not working as expected
def do_stuff(a, b):
    d = np.linalg.norm(a - b, axis=1)
    return sum(d) / len(d)


# TODO: Implement this function
def do_stuff2(a, b):
    pass


if __name__ == "__main__":
    vec_a = np.ones((1, 1))
    vec_b = np.array([])
    print(vec_a, vec_b)
    print(do_stuff(vec_a, vec_b))
    print(mean_euclidian_distance(vec_a, vec_b))
