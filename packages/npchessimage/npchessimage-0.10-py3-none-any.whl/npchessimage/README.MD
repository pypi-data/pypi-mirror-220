# Creates a chessboard pattern as an image.

## pip install npchessimage 

#### Tested against Windows 10 / Python 3.10 / Anaconda 

![](https://github.com/hansalemaos/screenshots/blob/main/testimage.png?raw=true)

```python
        

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
```