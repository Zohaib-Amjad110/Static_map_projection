import pandas as pd
import matplotlib.pyplot as plt

# Class for plotting location data on a map.
class LocationPlotter:
    # Constructor to initialize with CSV and image file paths.
    def __init__(self, locations_csv, map_image_file):
        self.locations_csv = locations_csv  # Path to the CSV file containing location data.
        self.map_image_file = map_image_file  # Path to the image file of the map.

    # Method to load location data from the CSV file.
    def load_locations(self):
        try:
            return pd.read_csv(self.locations_csv)  # Read and return data from the CSV file.
        except FileNotFoundError:  # Handle the case where the file is not found.
            print(f"Error: File not found - {self.locations_csv}.")
            return None
        except pd.errors.ParserError:  # Handle parsing errors in reading the CSV file.
            print(f"Error: Problem parsing the file - {self.locations_csv}.")
            return None

    # Method to filter the location data based on latitude and longitude boundaries.
    def filter_locations(self, location_data, lat_min, lat_max, lon_min, lon_max):
        if lat_min >= lat_max or lon_min >= lon_max:  # Validate the geographic bounds.
            print("Invalid latitude or longitude bounds.")
            return None
        # Return the filtered data based on the specified bounds.
        return location_data[
            (location_data['Longitude'] >= lon_min) & (location_data['Longitude'] <= lon_max) &
            (location_data['Latitude'] >= lat_min) & (location_data['Latitude'] <= lat_max)
        ]

    # Method to display the map with the filtered location data.
    def plot_map(self, filtered_data, lat_min, lat_max, lon_min, lon_max):
        fig, ax = plt.subplots()  # Create a Matplotlib figure and axis object.

        # Plot location data points on the map.
        ax.scatter(filtered_data['Latitude'], filtered_data['Longitude'], color='black')
        ax.set_title('Map of Sensor Locations')  # Set the title of the plot.
        ax.set_xlabel('Latitude')  # Label the x-axis as 'Latitude'.
        ax.set_ylabel('Longitude')  # Label the y-axis as 'Longitude'.

        # Try to load and display the background map image.
        try:
            map_img = plt.imread(self.map_image_file)  # Read the map image file.
            # Display the map image in the background with specified extent.
            ax.imshow(map_img, extent=[lat_min, lat_max, lon_min, lon_max], aspect='auto')
        except FileNotFoundError:  # Handle the case where the map image file is not found.
            print(f"Error: Map image file not found - {self.map_image_file}.")
            plt.close(fig)  # Close the Matplotlib figure.
            return
        plt.show()  # Display the plot.

# Main function to execute the script.
def main():
    # Define the geographic boundaries for the data.
    lat_lower, lat_upper = -10.592, 1.6848
    lon_lower, lon_upper = 50.681, 57.985 

    # Create an instance of LocationPlotter with CSV and map image file paths.
    plotter = LocationPlotter('GrowLocations.csv', 'map7.png')

    # Load the location data from the CSV file.
    location_data = plotter.load_locations()
    if location_data is None:  # Exit if data loading fails.
        return

    # Filter the location data based on defined geographic bounds.
    valid_locations = plotter.filter_locations(
        location_data, lat_lower, lat_upper, lon_lower, lon_upper)
    if valid_locations is None:  # Exit if data filtering fails.
        return

    # Plot the valid location data on the map.
    plotter.plot_map(valid_locations, lat_lower, lat_upper, lon_lower, lon_upper)

# Check if the script is run as the main program and call main().
if __name__ == "__main__":
    main()
