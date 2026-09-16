from benchmark.seeds import generate_seeds

def test_generate_seeds_count():
    seeds = generate_seeds(
        count=5,
        seed=12345,
    )

    assert len(seeds) == 5

def test_generate_seeds_is_reproducible():
    seeds_a = generate_seeds(
        count=5,
        seed=12345,
    )

    seeds_b = generate_seeds(
        count=5,
        seed=12345,
    )

    assert seeds_a == seeds_b

def test_generate_seeds_different_seeds():
    seeds_a = generate_seeds(
        count=5,
        seed=12345,
    )

    seeds_b = generate_seeds(
        count=5,
        seed=54321,
    )

    assert seeds_a != seeds_b

def test_generate_seeds_negative_count():
    try:
        generate_seeds(
            count=-1,
            seed=12345,
        )
    except ValueError:
        pass
    else:
        raise AssertionError(
            "Debe lanzar ValueError."
        )