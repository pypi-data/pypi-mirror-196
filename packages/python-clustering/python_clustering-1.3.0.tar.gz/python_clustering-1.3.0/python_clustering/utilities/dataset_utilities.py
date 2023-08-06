from typing import Tuple
from scipy import stats
from statistics import NormalDist
import numpy as np
from . import read_utilities


class Dataset:
    def __init__(self, dataset_name, path) -> None:
        self.name = dataset_name.split(".")[-2]
        self.pd_dataframe = read_utilities.load(
            self.name, path=f"{path}/{dataset_name}"
        )
        self.description = read_utilities.load_description(
            self.name, path=f"{path}/{dataset_name}"
        )
        self.origin = path.split("/")[-1]
        self.classes = (
            self.pd_dataframe["class"].unique()
            if "class" in self.pd_dataframe.columns
            else []
        )
        self.number_of_clusters = len(self.classes)
        if self.number_of_clusters == 1 and "class" in self.pd_dataframe.columns:
            self.pd_dataframe.drop("class", inplace=True, axis=1)
        self.dimensions = [x for x in self.pd_dataframe if x != "class"]
        self.std_dictionary, self.mean_dictionary = self.calculate_std_mean()
        self.number_of_datapoint = self.calculate_dataframe_shape(cols=False)
        self.number_of_dimensions = self.calculate_dataframe_shape(rows=False) - int(
            "class" in self.pd_dataframe.columns
        )
        self.missing_values_proportion = np.round(self.calculate_number_of_nan(), 4)
        self.is_imbalanced = None
        self.estimate_max_overlap, self.estimate_mean_overlap = None, None
        if self.number_of_clusters > 1:
            self.is_imbalanced = bool(self.calculate_is_imbalanced())
            (
                self.estimate_max_overlap,
                self.estimate_mean_overlap,
            ) = self.calculate_estimate_overlap()
        self.strong_outlier_proportion = np.round(
            self.calculate_number_of_outliers(number_of_std=3), 4
        )
        self.weak_outlier_proportion = np.round(
            (
                self.calculate_number_of_outliers(number_of_std=2)
                - self.strong_outlier_proportion
            ),
            4,
        )

    def calculate_number_of_nan(self) -> float:
        """Returning percentage of NaN(null) values

        Returns:
            float: percentage of NaN(null) values in self.df
        """
        return self.pd_dataframe.isnull().sum().sum() / self.pd_dataframe.size

    def calculate_std_mean(self) -> Tuple[dict, dict]:
        """Calculating std and mean per class in self.df

        Returns:
            Tuple[dict, dict]: mean and std dictionaries
        """
        if self.number_of_clusters > 1:
            return self.pd_dataframe.groupby("class").std().to_dict(
                "index"
            ), self.pd_dataframe.groupby("class").mean().to_dict("index")
        else:
            return self.pd_dataframe.std().to_dict(), self.pd_dataframe.mean().to_dict()

    def calculate_estimate_overlap(self, decimals: int = 4) -> Tuple[float, float]:
        """Calculating maxmimum and average overlap of clusters

        Args:
            decimals (int, optional): Rounding decimal points. Defaults to 4.

        Returns:
            Tuple[float, float]: maxmimum and average overlap of clusters
        """
        overlap_list = []
        for idx, cluster1 in enumerate(self.classes):
            for cluster2 in self.classes[idx + 1 :]:
                for dimension in self.dimensions:
                    overlap = NormalDist(
                        mu=self.mean_dictionary[cluster1][dimension],
                        sigma=np.nan_to_num(self.std_dictionary[cluster1][dimension])
                        + 1e-10,
                    ).overlap(
                        NormalDist(
                            mu=self.mean_dictionary[cluster2][dimension],
                            sigma=np.nan_to_num(
                                self.std_dictionary[cluster2][dimension]
                            )
                            + 1e-10,
                        )
                    )
                overlap_list.append(np.prod(overlap))
        return np.round(np.max(overlap_list), decimals), np.round(
            np.mean(overlap_list), decimals
        )

    def calculate_dataframe_shape(
        self, rows: bool = True, cols: bool = True
    ) -> int or None or Tuple[int, int]:
        """Returns shape of the dataframe based on rows and cols bool values

        Args:
            rows (bool, optional): Return number of rows. Defaults to True.
            cols (bool, optional): Return number of cols. Defaults to True.

        Returns:
            int or None or Tuple[int, int]: shape of df/params passed
        """
        if rows:
            if cols:
                return self.pd_dataframe.shape
            return self.pd_dataframe.shape[0]
        elif cols:
            return self.pd_dataframe.shape[1]
        return None

    def calculate_is_imbalanced(
        self, shapiro_alpha: float = 0.05, binary_alpha: float = 0.2
    ) -> bool:
        """Calculating if the clusters are imbalanced

        Args:
            shapiro_alpha (float, optional): stats.shapiro threshold. Defaults to 0.05.
            binary_alpha (float, optional): manual threshold for 2 classes. Defaults to 0.2.

        Returns:
            bool: _description_
        """
        if self.number_of_clusters == 2:
            return (
                self.pd_dataframe["class"].value_counts().min()
                / self.number_of_datapoint
                > binary_alpha
            )
        class_frequency = self.pd_dataframe["class"].value_counts().to_list()
        if [class_frequency[0]] * self.number_of_clusters == class_frequency:
            return False
        else:
            _, p = stats.shapiro(class_frequency)
            return p < shapiro_alpha

    def calculate_number_of_outliers(self, number_of_std: float = 2.0) -> float:
        """Calculating a percentage of outliers in clusters

        Args:
            number_of_std (float, optional): std threshold. Defaults to 2.0.

        Returns:
            float: percentage of outliers
        """
        if self.number_of_clusters > 1:
            return (
                self.pd_dataframe.groupby("class")
                .apply(lambda x: np.abs(stats.zscore(x) > number_of_std))
                .any(axis=1)
                .sum()
                / self.number_of_datapoint
            )
        else:
            return (
                self.pd_dataframe.apply(lambda x: np.abs(stats.zscore(x) > 2))
                .any(axis=1)
                .sum()
                / self.number_of_datapoint
            )


if __name__ == "__main__":
    pass
