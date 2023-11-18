import abc
import csv

from constants import PNG_PATH


class CsvWriter(metaclass=abc.ABCMeta):
    @abc.abstractclassmethod
    def write_header(cls) -> None:
        raise NotImplementedError()

    @abc.abstractclassmethod
    def write_row(cls, row) -> None:
        raise NotImplementedError()


class StatsCsvWriter(CsvWriter):
    fname = PNG_PATH + "evaluation_stats.csv"

    @classmethod
    def write_header(cls):
        with open(cls.fname, "a") as f:
            writer = csv.writer(f)
            writer.writerow(
                [
                    "NNmax",
                    "NNmin",
                    "NEmax",
                    "NEmin",
                    "EEmax",
                    "EEmin",
                    "NNave",
                    "NNstd",
                    "NEave",
                    "NEstd",
                    "EEave",
                    "EEstd",
                ]
            )

    @classmethod
    def write_row(cls, row):
        with open(cls.fname, "a") as f:
            writer = csv.writer(f)
            writer.writerow(row)


class ClutterCsvWriter(CsvWriter):
    fname = PNG_PATH + "clutter_each_generation.csv"

    @classmethod
    def write_header(cls):
        with open(cls.fname, "a") as f:
            writer = csv.writer(f)
            writer.writerow(
                ["gen", "scaled_clutter", "normalized_clutter", "standardized_clutter"]
            )

    @classmethod
    def write_row(cls, row):
        with open(cls.fname, "a") as f:
            writer = csv.writer(f)
            writer.writerow(row)
            writer.writerow(["------------"])