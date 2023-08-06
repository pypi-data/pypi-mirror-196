import pandas as pd
import matplotlib.pyplot as plt

class OrdersData:
    def __init__(self, dataset_path:str):
        self.__dataset_path = dataset_path
        self._df: pd.DataFrame = pd.read_csv(self.__dataset_path)

    def analyze_price_with_category(self):
        sub_df = self._df[['price', 'category_code']]
        print(sub_df.columns)
        # plt.figure()
        # ax = sub_df.plot.hist(bins=25, grid=False)
        # plt.show()


if __name__ == '__main__':
    dataset_path = './data/dataset.csv'
    data = OrdersData(dataset_path=dataset_path)
    data.analyze_price_with_category()