from dataclasses import dataclass
import importlib
import inspect
import pkgutil

from solvers.base import Solver

class SolverRegistryError(Exception):
    """Error relacionado con el registro de solvers."""

class SolverDiscoveryError(Exception):
    """Error durante el descubrimiento de solvers."""

@dataclass(frozen = True)
class SolverMetadata:
    name: str
    display_name: str
    description: str
    category: str

@dataclass(frozen = True)
class SolverInfo:
    metadata: SolverMetadata
    solver_class: type[Solver]

_SOLVERS: dict[str, type[Solver]] = {}

def register_solver(
        *,
        name: str,
        display_name: str,
        description: str,
        category: str,
):
    def decorator(solver_class: type[Solver]) -> type[Solver]:
        if not inspect.isclass(solver_class):
            raise SolverRegistryError("Solo se pueden registrar clases.")

        if not issubclass(solver_class, Solver):
            raise SolverRegistryError(f"{solver_class.__name__} debe heredar de Solver.")

        if not name.strip():
            raise SolverRegistryError("El nombre del solver no puede estar vacío")

        key = name.lower()

        if key in _SOLVERS:
            raise SolverRegistryError(f"Ya existe un solver regustrado: {name}")

        metadata = SolverMetadata(
            name = key,
            display_name = display_name,
            description = description,
            category = category,
        )

        _SOLVERS[key] = SolverInfo(
            metadata = metadata,
            solver_class = solver_class,
        )

        return solver_class

    return decorator

def discover_solvers(package_name: str = "solvers") -> None:
    try:
        package = importlib.import_module(package_name)
    except ImportError as exc:
        raise SolverDiscoveryError(f"No se pudo importar el paquete '{package_name}'") from exc

    if not hasattr(package, "__path__"):
        raise SolverDiscoveryError(f"'{package_name}' no es un paquete.")

    for module_info in pkgutil.iter_modules(package.__path__):
        module_name = module_info.name

        if module_name.startswith("_"):
            continue

        if module_name in {
            "base",
            "events",
            "registry"
        }:
            continue

        full_name = (f"{package_name}.{module_name}")

        try:
            importlib.import_module(full_name)
        except Exception as exc:
            raise SolverDiscoveryError(
                f"No se pudo cargar el solver '{full_name}'."
            ) from exc

def get_solvers() -> list[SolverInfo]:
    return list(_SOLVERS.values())

def get_solver_names() -> list[str]:
    return list(_SOLVERS.keys())

def get_solver(name: str) -> SolverInfo:
    key = name.lower()

    try:
        return _SOLVERS[key]
    except KeyError as exc:
        raise SolverRegistryError(f"Solver desconocido: {name}") from exc

def create_solver(name: str) -> Solver:
    info = get_solver(name)

    return info.solver_class()