def BubbleSort(array):
    # custom bubble sort for priority queue
    """
    :param array: list([], [])
    :return: sorted list
    """
    for i in range(len(array[0])):
        for j in range(i + 1, len(array[0])):
            if array[0][i] < array[0][j]:
                array[0][i], array[0][j] = array[0][j], array[0][i]  # for priority
                array[1][i], array[1][j] = array[1][j], array[1][i]  # for value
