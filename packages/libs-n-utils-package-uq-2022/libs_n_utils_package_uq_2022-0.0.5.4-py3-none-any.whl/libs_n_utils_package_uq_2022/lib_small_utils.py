# Last update: -08-2021


# ######################################################################################################################
import numpy as np


def random_hex_color(num_colors):
    random_colors = [
        f'#{x:02x}{y:02x}{z:02x}'
        for x, y, z in
        [np.random.choice(range(256), size=3)
         for _ in range(num_colors)]
    ]

    return random_colors