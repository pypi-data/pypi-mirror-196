"""The show command."""


from .base import Base

import os

import pyarrow.parquet as pq


class Show(Base):
    def run(self):
        filepath = self.options['<filename>']
        arrow_table = pq.read_table(filepath)
        dataframe = arrow_table.to_pandas()
        print("Number of Fields: ", len(dataframe.columns))
        print("Number of Rows: ", len(dataframe.index))
        print("\n")
        print("Field Names: \n", dataframe.columns)
        print("\n")
        print("Field Data Types: \n", dataframe.dtypes)
        print("\n")
        print("Data Head: \n", dataframe.head())
        print("\n")
        filesize = os.path.getsize(filepath)
        print("File Size: ", float(filesize / (1024 * 1024)), " MB")
        memory_usage = dataframe.memory_usage(index=True, deep=True).sum() 
        print("Memory Usage: ", float(memory_usage / (1024 * 1024)), " MB")
        print("Encoding Ratio: ", memory_usage / filesize)
