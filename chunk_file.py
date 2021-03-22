import pandas as pd


def chunk_excel(df, c=0, chunk_size=1000):
    chunk_collection = []
    shape = df.shape[0]
    steps = chunk_size
    while True:
        if shape - chunk_size >= 0:
            chunk_collection.append(df[c:chunk_size])
            c = chunk_size
            chunk_size += steps
        else:
            chunk_collection.append(df[c:shape])
            break
    return chunk_collection


if __name__ == '__main__':
    print(chunk_excel(pd.read_excel('amazonurl.xlsx')))
