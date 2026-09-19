# AI-Maze
## Packages
Agregar en **_pyproject.toml_** los directorios que van generandose dentro del apartado de paquetes.

## Ejecución de comandos CLI
- **poetry run pytest**: Ejecuta todos los test
- **poetry run dataset**: Genera un dataset con las especificaciones de dataset/run.py
    - Comando más robusto para generación de datasets para entrenamiento de ML.
    ```
    poetry run dataset `
        --generators recursive_backtracking,cyclic `
        --solvers bfs `
        --rows 20 `
        --cols 20 `
        --count 500 `
        --seed 42 `
        --output dataset/data/v6_exploration
    ```
    Genera 1000 muestras resuletas por _bfs_, de las cuales, 500 son generadas por _recursive backtracking_ y otras 500 por _cyclic_. 