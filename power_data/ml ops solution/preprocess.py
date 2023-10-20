import pandas as pd


class PreProcess:
    def __init__(self, data_path="power_data.csv"):
        df = pd.read_csv(data_path)
        df = df[['Datetime', 'Power_MWH']]
        # Convert the 'Datetime' column to datetime type
        df['Datetime'] = pd.to_datetime(df['Datetime'])

        # Group the data by date and calculate the sum of 'Power_MWH'
        sum_by_date = df.groupby(df['Datetime'].dt.date)['Power_MWH'].sum()
        self.df = sum_by_date.reset_index().rename(columns={'Datetime': 'ds', 'Power_MWH': 'y'})[['ds', 'y']]

    def create_test_train_dataset_by_ratio(self, ratio=0.3):
        num_rows = int(len(self.df) * ratio)
        df_test = self.df.tail(num_rows)
        df_train = self.df.head(len(self.df) - num_rows)
        return df_train, df_test
