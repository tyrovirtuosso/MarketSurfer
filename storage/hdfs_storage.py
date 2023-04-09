from .abstract_storage import AbstractStorage
# from hdfs import InsecureClient
# libjvm_path = "/Library/Java/JavaVirtualMachines/jdk1.8.0_361.jdk/Contents/Home/jre/lib/server/"
# os.environ["ARROW_LIBHDFS_DIR"] = libjvm_path

import os

os.environ['JAVA_HOME'] = "/Library/Java/JavaVirtualMachines/jdk1.8.0_361.jdk/Contents/Home/jre"
os.environ['LD_LIBRARY_PATH'] = "/Library/Java/JavaVirtualMachines/jdk1.8.0_361.jdk/Contents/Home/jre"

# import pyarrow.fs

# import pyarrow as pa
# import pyarrow.parquet as pq
# import pandas as pd
# from pyarrow import dataset as ds


class HDFSStorage(AbstractStorage):
    def __init__(self, hdfs_uri="http://localhost:9870", base_path="/data"):
        # self.client = InsecureClient(hdfs_uri)
        self.base_path = base_path
        self.hdfs_uri = hdfs_uri

    def check_data_exists(self, symbol):
        # Implementation for checking if data exists in the HDFS
        pass

    def save_data(self, symbol, data):
        # Implementation for saving data to the HDFS
        print(os.environ['JAVA_HOME'])

        # Connect to the HDFS
        # fs = pyarrow.fs.HadoopFileSystem(host='localhost', port=9870)


        
        # # data['date'] = pd.to_datetime(data.index.date)
        # data['date'] = pd.to_datetime(data['date']).dt.date
        
        # # Prepare a destination path for the partitioned data
        # destination_path = f'{self.base_path}/crypto/{symbol}.parquet'


        # # Define a ParquetDataset
        # table = pa.Table.from_pandas(data)

        # # Define a partitioning schema
        # partitioning = ds.partitioning(
        #     pa.schema([
        #         ("category", pa.string()),
        #         ("source", pa.string()),
        #         ("symbol", pa.string())
        #     ])
        # )
        # # Write the dataset to HDFS
        # ds.write_dataset(table, destination_path, format='parquet', filesystem=fs, partitioning=partitioning)
     
        
        
        
        
        # Construct the HDFS path using the current working directory
        # current_directory = os.getcwd()
        # hdfs_folder = 'hdfs'
        
        # # Create the folder if it does not exist
        # os.makedirs(os.path.join(current_directory, hdfs_folder), exist_ok=True)
        # hdfs_path = os.path.join(current_directory, hdfs_folder, f'{symbol}.parquet')
        # self.save_to_hdfs(processed_data, hdfs_path)

    def load_data(self, symbol):
        # Implementation for loading data from the HDFS
        pass
