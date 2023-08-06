import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder


class AutoCorrFeatureSelection:
    """
    AutoCorrFeatureSelection is a class that performs automatic feature selection based on correlation analysis.
    """

    def __init__(self, data: pd.DataFrame) -> None:
        """
        Initializes the AutoCorrFeatureSelection instance.

        Args:
            data (pd.DataFrame): The input DataFrame containing the features.
        """

        self.__data = data
        self.__correlation_matrix = self.__calculate_correlation_matrix(data)

    def __calculate_correlation_matrix(self, df):
        encoded_df = self.__label_encode(df)
        correlation_matrix = encoded_df.corr()
        return correlation_matrix

    def __label_encode(self, df):
        string_columns = df.select_dtypes(include=["object"]).columns

        encoded_df = df.copy()
        label_encoder = LabelEncoder()

        for col in string_columns:
            encoded_df[col] = label_encoder.fit_transform(df[col])

        return encoded_df

    def correlation_matrix(self) -> pd.DataFrame:
        """
        Returns the correlation matrix of the features.

        Returns:
            pd.DataFrame: The correlation matrix of the features.
        """

        return self.__correlation_matrix

    def select_columns_above_threshold(self, threshold: float = 0.85) -> list:
        """
        Selects columns with a correlation above the specified threshold.

        Args:
            threshold (float, optional): The correlation threshold. Defaults to 0.85.

        Returns:
            list: A list of column names with correlation above the threshold.
        """

        selected_columns = []
        remaining_columns = [i for i in range(len(self.__data.columns))]

        while len(remaining_columns):

            # Store the correlation hit count for each column
            correlation_counts = {}

            for i in remaining_columns:

                # Count the number of columns with a correlation greater than the threshold
                corr_matrix = self.correlation_matrix()
                count = np.sum(abs(corr_matrix.iloc[i]) >= threshold)
                correlation_counts[i] = count

            if not correlation_counts:
                break

            # Get the column with the highest number of matches
            max_column = max(
                correlation_counts,
                key=lambda x, cc=correlation_counts: (cc[x], self.__data.columns[x]),
                default=None,
            )

            if max_column is None:
                break

            selected_columns.append(max_column)

            # Discard the selected column and the adjacent ones for the next iterations
            remaining_columns.remove(max_column)

            for idx, val in enumerate(self.correlation_matrix().iloc[max_column]):
                if abs(val) >= threshold and idx in remaining_columns:
                    remaining_columns.remove(idx)

        return [self.__data.columns[i] for i in selected_columns]
