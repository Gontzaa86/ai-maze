from dataclasses import dataclass

from dataset.record import DatasetRecord

@dataclass(frozen = True)
class DatasetSplit:
    train: tuple[DatasetRecord, ...]
    validation: tuple[DatasetRecord, ...]
    test: tuple[DatasetRecord, ...]

class DatasetSplitter:
    """
    Divide un dataset en train, validation y test.

    La división se realiza sobre DatasetRecord completos.
    Las muestras de ML se generan posteriormente, evitando que estados del mismo laberinto aparezcan en distintos splits.
    """

    def split(
            self,
            records: list[DatasetRecord],
            *,
            train_ratio: float = 0.70,
            validation_ratio: float = 0.15,
            test_ratio: float = 0.15,
            seed: int = 42
    ) -> DatasetSplit:
        self._validate_ratios(train_ratio, validation_ratio, test_ratio)

        shuffled = list(records)
        self._shuffle(shuffled, seed)

        total = len(shuffled)

        train_count = int(total * train_ratio)
        validation_count = int(total * validation_ratio)

        train_end = train_count
        validation_end = train_count + validation_count

        return DatasetSplit(
            train = tuple(shuffled[:train_end]),
            validation = tuple(shuffled[train_end:validation_end]),
            test = tuple(shuffled[validation_end:])
        )

    def _shuffle(self, records: list[DatasetRecord], seed: int) -> None:
        import random

        rng = random.Random(seed)
        rng.shuffle(records)

    def _validate_ratios(self, train_ratio: float, validaiton_ratio: float, test_ratio: float) -> None:
        ratios = (train_ratio, validaiton_ratio, test_ratio)

        if any(ratio < 0 or ratio > 1 for ratio in ratios):
            raise ValueError("Las proporciones deben estar entre 0 y 1.")

        if abs(sum(ratios) - 1.0) > 1e-9:
            raise ValueError("Las proporciones deben sumar 1.")