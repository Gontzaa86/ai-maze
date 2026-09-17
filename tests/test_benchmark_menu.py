import pygame # type: ignore

from visualization.benchmark_menu import BenchmarkMenu

from generators.registry import discover_generators
from solvers.registry import discover_solvers

discover_generators()
discover_solvers()

def test_benchmark_menu_has_generators_and_solvers():
    pygame.init()

    menu = BenchmarkMenu()

    assert menu.generators
    assert menu.solvers

    pygame.quit()

def test_benchmark_menu_default_configuration():
    pygame.init()

    menu = BenchmarkMenu()

    configuration = menu._create_configuration()

    assert configuration["rows"] == 20
    assert configuration["cols"] == 20
    assert configuration["generator"] == (
        menu.generators[0].metadata.name
    )
    assert configuration["solver"] == (
        menu.solvers[0].metadata.name
    )
    assert configuration["seed"] is None
    assert configuration["seed_count"] == 10

    pygame.quit()

def test_benchmark_menu_seed_configuration():
    pygame.init()

    menu = BenchmarkMenu()

    menu.seed = "12345"

    configuration = menu._create_configuration()

    assert configuration["seed"] == 12345

    pygame.quit()

def create_menu():
    pygame.init()
    return BenchmarkMenu()

def test_benchmark_menu_custom_run_count():
    menu = create_menu()

    menu.runs = "100"

    configuration = menu._create_configuration()

    assert configuration is not None
    assert configuration["seed_count"] == 100