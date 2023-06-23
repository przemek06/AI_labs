import pandas as pd
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.model_selection import train_test_split

def split_data(df):
    # training_df = df.sample(frac=0.7, random_state=42)  # 70% of the original DataFrame
    # validation_df = df.sample(frac=0.2, random_state=42)  # 20% of the original DataFrame
    # test_df = df.sample(frac=0.1, random_state=42)  # 10% of the original DataFrame

    training_df, validation_df = train_test_split(df, train_size=0.7, test_size=0.3, random_state=41)
    validation_df, test_df = train_test_split(validation_df, train_size=0.6, test_size=0.4, random_state=41)

    return training_df, validation_df, test_df

def split_columns(df):
    middle_columns = df.columns[1:-1]
    last_column = df.columns[-1]

    X = df[middle_columns]
    Y = df[last_column]
    
    return X, Y

def normalize_data(df):
    scaler = MinMaxScaler()
    columns_to_normalize = df.columns[1:-1]
    df_normalized = pd.DataFrame(df)
    df_normalized[columns_to_normalize] = scaler.fit_transform(df[columns_to_normalize])
    return df_normalized


def standardize_data(df):
    scaler = StandardScaler()
    columns_to_standardize = df.columns[1:-1]
    df_standardized = pd.DataFrame(df)
    df_standardized[columns_to_standardize] = scaler.fit_transform(df[columns_to_standardize])
    return df_standardized