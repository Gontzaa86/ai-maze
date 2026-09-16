import random

def generate_seeds(count: int, seed: int | None = None) -> list[int]:
    if count < 0:
        raise ValueError("El número de seeds no puede ser negativo.")

    random_generator = random.Random(seed)

    return [
        random_generator.randint(0, 2**32 - 1)
        for _ in range(count)
    ]