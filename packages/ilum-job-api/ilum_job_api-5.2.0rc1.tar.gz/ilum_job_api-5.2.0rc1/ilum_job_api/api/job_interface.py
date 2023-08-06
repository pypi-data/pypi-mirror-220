from abc import ABC, abstractmethod
from pyspark.sql import SparkSession


class Job(ABC):
    """
    ilum interactive job interface representing one result calculation
    """

    @abstractmethod
    def run(self, spark_session: SparkSession, config: dict) -> str:
        """
        run method used to interact with long living spark job
        :param spark_session configured spark session to be shared between single calculations
        :param config configuration to be applied for a single calculation
        :return string representation of produced result (user should care about serialization), or None if missing
        """
        pass
