import numpy as np
from math import ceil


def get_iter_rotate_right(l, n, onlyfinal=False):
    """
    Generate iterations of a list rotated to the right.

    Args:
        l (list): The input list.
        n (int): The number of rotations.
        onlyfinal (bool, optional): If True, only the final iteration is returned. Defaults to False.

    Yields:
        list: The rotated list at each iteration.

    Returns:
        list: The final rotated list if onlyfinal is True.

    Example:
        l = [1, 2, 3, 4, 5]
        rotations = 3

        for iteration in get_iter_rotate_right(l, rotations):
            print(iteration)

        # Output:
        # [5, 1, 2, 3, 4]
        # [4, 5, 1, 2, 3]
        # [3, 4, 5, 1, 2]

        final_iteration = get_iter_rotate_right(l, rotations, onlyfinal=True)
        print(final_iteration)

        # Output:
        # [3, 4, 5, 1, 2]
    """

    iterable_ = l.copy()

    for _ in range(n):
        iterable_ = iterable_[-1:] + iterable_[:-1]
        if not onlyfinal:
            yield iterable_
    if onlyfinal:
        yield iterable_


def create_new_image(width, height, color=(0, 0, 0)):
    """
    Create a new image with the specified width, height, and color.

    Args:
        width (int): The width of the image.
        height (int): The height of the image.
        color (tuple, optional): The RGB color value for the image. Defaults to (0, 0, 0).

    Returns:
        numpy.ndarray: The new image as a NumPy array.

    Example:
        new_image = create_new_image(100, 200, color=(255, 255, 255))
        print(new_image.shape)

        # Output:
        # (200, 100, 3)
    """

    color = np.array(list(reversed(color)), dtype=np.uint8)
    emptyimage = color * np.ones((height, width, len(color)), np.uint8)
    return emptyimage


def create_chessboard(
    block_size=10,
    width=1000,
    height=1000,
    colors=((0, 0, 0), (255, 0, 0), (255, 255, 0)),
):
    r"""
        Create a chessboard pattern as an image.

        Args:
            block_size (int, optional): The size of each square block on the chessboard. Defaults to 10.
            width (int, optional): The total width of the chessboard image. Defaults to 1000.
            height (int, optional): The total height of the chessboard image. Defaults to 1000.
            colors (tuple or list, optional): The RGB color values for the chessboard. Defaults to ((0, 0, 0), (255, 0, 0), (255, 255, 0)).

        Returns:
            numpy.ndarray: The generated chessboard image as a NumPy array.

        Example:
            from npchessimage import create_chessboard

            chessboard = create_chessboard(block_size=20, width=800, height=600, colors=((255, 255, 255), (0, 0, 0)))
            print(chessboard.shape)

            # Output:
            # (600, 800, 3)

            img = create_chessboard(
                block_size=10,
                width=200,
                height=300,
                colors=((0, 0, 0), (255, 0, 0), (255, 255, 0)),
            )
            import cv2
            cv2.imwrite('c:\\testimage.png',img)
    """

    alli = []
    for color in colors:
        alli.append(create_new_image(width=block_size, height=block_size, color=color))

    ali = np.vstack(
        [np.hstack(x) for x in get_iter_rotate_right(alli, len(alli), onlyfinal=False)]
    )
    ali2 = np.hstack(
        [
            np.vstack([ali for x in range(ceil(width / ali.shape[1]))])
            for y in range(ceil(height / ali.shape[0]))
        ]
    )
    return ali2[:width, :height]
