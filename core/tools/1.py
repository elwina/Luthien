import numpy as np

a = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
b = list(
    map(
        lambda row: (" ".join(map(lambda x: str(x), row)) + "\n"),
        a,
    )
)
print(b)
