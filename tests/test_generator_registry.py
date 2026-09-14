import pytest # type: ignore

from generators.recursive_backtracking import RecursiveBacktrackingGenerator
from generators.registry import GeneratorRegistryError, create_generator, discover_generators, get_generator, get_generator_names, register_generator

discover_generators()

def test_recursive_backtracking_is_registered():
    assert "recursive_backtracking" in get_generator_names()

def test_cyclic_is_registered():
    assert "cyclic" in get_generator_names()

def test_create_recursive_backtracking():
    generator = create_generator(
        "recursive_backtracking"
    )

    assert isinstance(generator, RecursiveBacktrackingGenerator)

def test_create_generator_is_case_insensitive():
    generator = create_generator("CYCLIC")

    assert generator.__class__.__name__ == ("CyclicMazeGenerator")

def test_unknown_generator():
    with pytest.raises(GeneratorRegistryError):
        create_generator("inexistente")

def test_register_custom_generator():
    @register_generator(
        name="dummy",
        display_name="Dummy Generator",
        description="Generador utilizado para probar la extensibilidad.",
        category="test",
    )
    class DummyGenerator:

        def generate(self, rows, cols):
            return None

    info = get_generator("dummy")

    assert info.metadata.name == "dummy"
    assert info.metadata.display_name == "Dummy Generator"
    assert info.metadata.description == (
        "Generador utilizado para probar la extensibilidad."
    )
    assert info.metadata.category == "test"

    generator = create_generator("dummy")

    assert isinstance(generator, DummyGenerator)

def test_register_duplicate_generator():
    @register_generator(
        name="duplicate",
        display_name="Duplicate",
        description="Primer generador.",
        category="test",
    )
    class FirstGenerator:

        def generate(self, rows, cols):
            return None

    with pytest.raises(GeneratorRegistryError):

        @register_generator(
            name="duplicate",
            display_name="Another",
            description="Segundo generador.",
            category="test",
        )
        class SecondGenerator:

            def generate(self, rows, cols):
                return None

def test_register_invalid_generator():
    with pytest.raises(GeneratorRegistryError):

        @register_generator(
            name="invalid",
            display_name="Invalid",
            description="No implementa generate.",
            category="test",
        )
        class InvalidGenerator:
            pass

def test_register_empty_name():
    with pytest.raises(GeneratorRegistryError):

        @register_generator(
            name="   ",
            display_name="Invalid",
            description="Nombre vacío.",
            category="test",
        )
        class EmptyNameGenerator:

            def generate(self, rows, cols):
                return None