import pandas as pd
import numpy as np
from functools import reduce

class Coolmap:
    def __init__(self, dataframe):
        self.dataframe = dataframe

    def prepare_task_status_data(self, column_list):
        data = self.dataframe
        data = data.dropna(axis=0, subset=['task_status'])
        data.loc[:, column_list] = data.loc[:, column_list].fillna('')
        data = data.groupby(column_list).agg({'counts':'sum'}).reset_index()
        data_incomplete = data.loc[data.task_status == 'Incomplete'].drop('task_status', axis=1)
        data_open = data.loc[data.task_status == 'Open'].drop('task_status', axis=1)
        data_ongoing = data.loc[~data.task_status.isin(['Incomplete', 'Open', 'Done'])].drop('task_status', axis=1)
        column_list.remove('task_status')

        data_ongoing = data_ongoing.groupby(column_list, as_index=False).sum()
        data_done = data.loc[data.task_status == 'Done'].drop('task_status', axis=1)
        data_incomplete = data_incomplete.rename(columns={'counts': 'Incomplete'})
        data_open = data_open.rename(columns={'counts': 'Open'})
        data_ongoing = data_ongoing.rename(columns={'counts': 'Ongoing'})
        data_done = data_done.rename(columns={'counts': 'Done'})
        data_frames = [data_incomplete, data_open, data_ongoing, data_done]
        data_merged = reduce(lambda left, right: pd.merge(left, right, on=column_list, how='outer'), data_frames)
        data_merged = data_merged.fillna(0)

        data_merged[data_merged.columns.difference(column_list)] = data_merged[
            data_merged.columns.difference(column_list)].astype(int)

        data_merged['Total'] = data_merged.drop(column_list, axis=1).sum(axis=1)

        return data_merged.sort_values('order_number', ascending=True).T.to_dict()
    


    def prepare_driver_data(self, column_list):
        data = self.dataframe
        data.loc[:, column_list] = data.loc[:, column_list].fillna('')
        data = data.groupby(column_list).agg({'counts':'sum'}).reset_index()
        data['driver_name'].replace('', np.nan, inplace=True)
        data = data.drop(['counts'], axis=1)
        data = data.dropna(axis=0, subset=['driver_name'])
        d = data.T.to_dict()
        driver_result = list(d.values())

        driver_details = {} 
        for each in driver_result:
            temp_dict = each
            order_number = each['order_number']
            temp_lst = driver_details.get(order_number, [])
            del temp_dict['order_number']
            temp_lst.append(temp_dict)
            driver_details[order_number] = temp_lst

        return driver_details