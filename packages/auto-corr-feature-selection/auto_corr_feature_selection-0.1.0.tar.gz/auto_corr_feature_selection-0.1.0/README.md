# AutoCorrFeatureSelection

Automatically select the most relevant features based on correlation.


# How it works

The __AutoCorrFeatureSelection__ class utilizes correlation analysis to automatically select relevant features from a given dataset. Here's a step-by-step overview of how it works:

1. Correlation Matrix:

The first step is to calculate the correlation matrix, which measures the pairwise correlation between all features in the dataset. The correlation matrix provides insight into the relationships between the features.


|              | sepal.length | sepal.width | petal.length | petal.width | variety |
|:------------:|:------------:|:-----------:|:------------:|:-----------:|:-------:|
| sepal.length |      1.0     |    -0.11    |     0.87     |     0.81    |   0.72  |
|  sepal.width |     -0.11    |     1.0     |     -0.42    |    -0.36    |  -0.42  |
| petal.length |     0.87     |    -0.42    |      1.0     |     0.96    |   0.94  |
|  petal.width |     0.81     |    -0.36    |     0.96     |     1.0     |   0.95  |
|    variety   |     0.72     |    -0.42    |     0.94     |     0.95    |   1.0   |


2. Threshold-based Selection:

Next, the class applies a threshold to the correlation matrix to identify columns with correlations above the specified threshold (for example 0.85). These columns are considered highly correlated and may contain redundant or similar information.


|              | sepal.length | sepal.width | petal.length | petal.width | variety |
|:------------:|:------------:|:-----------:|:------------:|:-----------:|:-------:|
| sepal.length |              |             |     0.87     |             |         |
|  sepal.width |              |             |              |             |         |
| petal.length |     0.87     |             |              |     0.96    |   0.94  |
|  petal.width |              |             |     0.96     |             |   0.95  |
|    variety   |              |             |     0.94     |     0.95    |         |


3. Selected Columns and Relationships:

The selected columns are visually represented, showcasing the relationships between the highly correlated features. This diagram helps visualize the interconnectedness of these features.

![iris_corr_diagram](resources/img/iris_corr_diagram.png)

By following these steps, the AutoCorrFeatureSelection class automates the process of feature selection based on correlation analysis, enabling you to identify and focus on the most informative and non-redundant features in your dataset.


# Example

Examples can be found in [examples/](examples/).

```python

# set up auto correlation
auto_corr = AutoCorrFeatureSelection(df)

# select low correlated columns
selected_columns = auto_corr.select_columns_above_threshold(threshold=0.85)
filtered_df = df[selected_columns]

```
