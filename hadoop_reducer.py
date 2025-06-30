#!/usr/bin/env python3

import sys

def main():
    """
    Hadoop Reducer for calculating min, max, and average of sensor values.
    Assumes input values are already filtered by the mapper based on location.
    """
    total_sum = 0.0
    count = 0
    min_value = float('inf')
    max_value = float('-inf')

    for line in sys.stdin:
        try:
            # The mapper is expected to output just the value, e.g., "25.25"
            value = float(line.strip())

            total_sum += value
            count += 1
            min_value = min(min_value, value)
            max_value = max(max_value, value)

        except ValueError:
            # Skip lines that cannot be converted to float (e.g., malformed data)
            continue
        except Exception as e:
            # Log other exceptions for debugging, if necessary
            sys.stderr.write(f"Error processing line: {line.strip()} - {e}\n")
            continue

    if count > 0:
        average = total_sum / count
        # Output the results in a clear format
        print(f"Minimum Value: {min_value}")
        print(f"Maximum Value: {max_value}")
        print(f"Average Value: {average}")
    else:
        print("No valid data received for aggregation.")

if __name__ == "__main__":
    main()