import pandas as pd

glass_types = {
    1: 'building_windows_float_processed',
    2: 'building_windows_non_float_processed',
    3: 'vehicle_windows_float_processed',
    4: 'vehicle_windows_non_float_processed',
    5: 'containers',
    6: 'tableware',
    7: 'headlamps'
}

glass_data_labels = {
    1: "Id number",
    2: "Refractive index",
    3: "Sodium",
    4: "Magnesium",
    5: "Aluminum",
    6: "Silicon",
    7: "Potassium",
    8: "Calcium",
    9: "Barium",
    10: "Iron",
    11: "Type of glass"
}


def read_data(file_name):
    df = pd.read_csv(file_name)
    return df

def show_averages_of_data(df):
    row_avg = df.mean()[1:-1]

    for i, avg in enumerate(row_avg):
        print("Average value for " + str(glass_data_labels[i+2]) + ": " + str(avg))

def show_distribution_of_types(df):
    distributions = {}

    for i in range(1, 8):
        filtered_df = df[df.iloc[:, 10] == i]
        distributions[i] = filtered_df.size / df.size

    for i, distribution in distributions.items():
        print("Distribution of " + glass_types[i] + " in glass dataset: " + str(distribution))


