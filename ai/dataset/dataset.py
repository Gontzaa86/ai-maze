from dataclasses import dataclass

from dataset.record import DatasetRecord

from ai.dataset.builder import TrainingSampleBuilder
from ai.dataset.sample import Action, TrainingSample
from ai.dataset.split import DatasetSplit, DatasetSplitter

@dataclass(frozen=True)
class DatasetStatistics:
    records: int
    samples: int
    actions: dict[Action, int]

@dataclass(frozen=True)
class MLDataset:
    train_records: tuple[DatasetRecord, ...]
    validation_records: tuple[DatasetRecord, ...]
    test_records: tuple[DatasetRecord, ...]

    train_samples: tuple[TrainingSample, ...]
    validation_samples: tuple[TrainingSample, ...]
    test_samples: tuple[TrainingSample, ...]

    @classmethod
    def from_records(
        cls,
        records: list[DatasetRecord],
        *,
        train_ratio: float = 0.70,
        validation_ratio: float = 0.15,
        test_ratio: float = 0.15,
        seed: int = 42,
    ) -> "MLDataset":
        splitter = DatasetSplitter()

        split = splitter.split(
            records,
            train_ratio=train_ratio,
            validation_ratio=validation_ratio,
            test_ratio=test_ratio,
            seed=seed,
        )

        builder = TrainingSampleBuilder()

        train_samples = cls._build_samples(split.train, builder)
        validation_samples = cls._build_samples(split.validation, builder)
        test_samples = cls._build_samples(split.test, builder)

        return cls(
            train_records=split.train,
            validation_records=split.validation,
            test_records=split.test,
            train_samples=tuple(train_samples),
            validation_samples=tuple(validation_samples),
            test_samples=tuple(test_samples),
        )

    @staticmethod
    def _build_samples(
        records: tuple[DatasetRecord, ...],
        builder: TrainingSampleBuilder,
    ) -> list[TrainingSample]:
        samples = []

        for record in records:
            samples.extend(builder.build(record))

        return samples

    def train_statistics(self) -> DatasetStatistics:
        return self._statistics(
            self.train_records,
            self.train_samples,
        )

    def validation_statistics(self) -> DatasetStatistics:
        return self._statistics(
            self.validation_records,
            self.validation_samples,
        )

    def test_statistics(self) -> DatasetStatistics:
        return self._statistics(
            self.test_records,
            self.test_samples,
        )

    def _statistics(
        self,
        records: tuple[DatasetRecord, ...],
        samples: tuple[TrainingSample, ...],
    ) -> DatasetStatistics:
        actions = {
            Action.UP: 0,
            Action.RIGHT: 0,
            Action.DOWN: 0,
            Action.LEFT: 0,
        }

        for sample in samples:
            actions[sample.action] += 1

        return DatasetStatistics(
            records=len(records),
            samples=len(samples),
            actions=actions,
        )