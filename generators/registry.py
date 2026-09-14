from dataclasses import dataclass
import importlib
import inspect
import pkgutil

class GeneratorRegistryError(Exception):
    """Error relacionado con el registro de generadores."""

class GeneratorDiscoveryError(GeneratorRegistryError):
    """Error durante el descubrimiento de generadores."""

@dataclass(frozen = True)
class GeneratorMetadata:
    name: str
    display_name: str
    description: str
    category: str

@dataclass(frozen = True)
class GeneratorInfo:
    metadata: GeneratorMetadata
    generator_class: type

_GENERATORS: dict[str, GeneratorInfo] = {}

def register_generator(
        *,
        name: str,
        display_name: str,
        description: str,
        category: str,
):
    def decorator(generator_class: type) -> type:
        if not inspect.isclass(generator_class):
            raise GeneratorRegistryError("Solo se pueden registrar clases.")

        if not hasattr(generator_class, "generate"):
            raise GeneratorRegistryError(f"{generator_class.__name__} debe implementar el método generate().")

        if not name.strip():
            raise GeneratorRegistryError("El nombre del generador no puede estar vacío.")

        key = name.lower()

        if key in _GENERATORS:
            raise GeneratorRegistryError(f"Ya existe un generador registrado: {name}")

        metadata = GeneratorMetadata(
            name = key,
            display_name = display_name,
            description = description,
            category = category,
        )

        _GENERATORS[key] = GeneratorInfo(
            metadata = metadata,
            generator_class = generator_class
        )

        return generator_class

    return decorator

def discover_generators(package_name: str = "generators") -> None:
    try:
        package = importlib.import_module(package_name)
    except ImportError as exc:
        raise GeneratorDiscoveryError(f"No se pudo importar el paquete '{package_name}'.") from exc

    if not hasattr(package, "__path__"):
        raise GeneratorDiscoveryError(f"'{package_name}' no es un paquete.")

    for module_info in pkgutil.iter_modules(package.__path__):
        module_name = module_info.name

        if module_name.startswith("_"):
            continue

        if module_name in {
            "cell",
            "maze",
            "registry"
        }:
            continue

        full_name = (f"{package_name}.{module_name}")

        try:
            importlib.import_module(full_name)
        except Exception as exc:
            raise GeneratorDiscoveryError(f"No se pudo cargar el generador '{full_name}'.") from exc

def get_generators() -> list[GeneratorInfo]:
    return list(_GENERATORS.values())

def get_generator_names() -> list[str]:
    return list(_GENERATORS.keys())

def get_generator(name: str) -> GeneratorInfo:
    key = name.lower()

    try:
        return _GENERATORS[key]
    except KeyError as exc:
        raise GeneratorRegistryError(f"Generador desconocido: {name}") from exc

def create_generator(name: str, **kwargs):
    info = get_generator(name)

    return info.generator_class(**kwargs)