import numpy as np
import pandas as pd
test_file = "path/to/test_data.csv"

# Function to calculate the number of decimal places in a value
def count_decimal_places(value):
    if np.isnan(value):
        return 0
    text = f"{value:.10f}"  # Represent the number as a string with up to 10 decimal places
    if '.' in text:
        return len(text.split('.')[1].rstrip('0'))  # Count digits after decimal point
    return 0

# Function to calculate the non-diagonal neighbors' mean and match decimal places
def interpolate_missing_value(data, row, col):
    rows, cols = data.shape

    neighbors = [
        (row - 1, col),  # Top
        (row + 1, col),  # Bottom
        (row, col - 1),  # Left
        (row, col + 1)   # Right
    ]

    valid_neighbors = []
    decimal_places = []

    # Check for valid neighbors (within bounds and not NaN)
    for r, c in neighbors:
        if 0 <= r < rows and 0 <= c < cols and not np.isnan(data[r, c]):
            valid_neighbors.append(data[r, c])
            decimal_places.append(count_decimal_places(data[r, c]))

    # Calculate the mean of valid non-diagonal neighbors
    if valid_neighbors:
        mean_value = np.mean(valid_neighbors)
        # Determine the max number of decimal places among the neighbors
        max_decimal_places = max(decimal_places, default=0)
        # Round the mean to the appropriate number of decimal places
        return round(mean_value, max_decimal_places)
    else:
        return np.nan  # If no valid neighbors, leave it as NaN for now

# Load the input data
input_file = test_file
data = pd.read_csv(input_file, header=None).to_numpy()

# Perform iterative interpolation
def iterative_interpolation(data):
    missing_count = np.sum(np.isnan(data))  # Count how many NaN values remain
    prev_missing_count = -1  # To track changes in each iteration

    # Repeat until no more NaN values can be filled or no changes occur
    while missing_count > 0 and missing_count != prev_missing_count:
        prev_missing_count = missing_count

        # Iterate over the entire dataset
        for i in range(data.shape[0]):
            for j in range(data.shape[1]):
                if np.isnan(data[i, j]):
                    # Try to interpolate this NaN value
                    interpolated_value = interpolate_missing_value(data, i, j)
                    if not np.isnan(interpolated_value):
                        data[i, j] = interpolated_value

        # Recalculate how many NaN values remain
        missing_count = np.sum(np.isnan(data))

# Perform the iterative interpolation
iterative_interpolation(data)

# Write the interpolated data to a new CSV file
output_file = 'test_results.csv'
pd.DataFrame(data).to_csv(output_file, header=False, index=False)

print(f'Iteratively interpolated data saved to {output_file}')
