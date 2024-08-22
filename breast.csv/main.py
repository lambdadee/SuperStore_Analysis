import pandas as pd


def get_clean_data():
    data = pd.read_csv("data.csv")


def main():
    data = get_clean_data()



if __name__ == "__main__":
    main()