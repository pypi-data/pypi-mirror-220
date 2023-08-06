# captures and processes network packets asynchronously using the Scapy library, and converts the results to a pandas DataFrame

## pip install pdsniff 

#### Tested against Windows 10 ( Necessary: https://npcap.com/#download )  / Python 3.10 / Anaconda 

### Function start_sniffing

The start_sniffing function is designed to capture and process network packets asynchronously using the Scapy library. 
It takes several parameters, including count, result_list, killkey, and dumpfolder, to control the packet capturing and processing behavior.

#### Here's what the function does:

It initializes the result_list as a deque with a maximum length of 1 if not provided by the caller.
If a dumpfolder is provided, it creates the folder if it doesn't exist and determines the starting 
index for saving pickled files based on existing files in the folder.
It defines an internal function \_get_frame that handles the actual packet capturing and processing.
The packet capturing is done using a separate thread (KThread) to avoid blocking the main program execution.
Packets are captured and processed in batches of size count.
The processed data is converted into a pandas DataFrame with proper data types based on the provided dtypes.
If a dumpfolder is provided, the processed data frames are periodically saved as pickled files.

```python
    Args:
        count (int): The number of packets to capture and process in each batch.
        result_list (None, list, deque, optional): List or deque to store the processed data frames.
            If None, a deque with a maximum length of 1 will be used. Defaults to None.
        killkey (str, optional): The hotkey combination to stop packet capturing and processing.
            Defaults to "ctrl+alt+x".
        dumpfolder (str, optional): The folder path to save processed data frames as pickled files.
            If provided, captured packets will be periodically saved as pickle files in this folder.
            Defaults to None.
        **kwargs: Additional keyword arguments to be passed to the Scapy sniff function.

    Returns:
        KThread: A thread object that captures and processes the network packets.

    Note:
        This function starts a new thread (KThread) for packet capturing and processing. The function
        will keep running and capturing packets until the specified `killkey` hotkey is pressed.
        Captured packets will be processed in batches of `count` and stored in the `result_list`.
        If `dumpfolder` is provided, the processed data frames will also be saved as pickle files.

        The `result_list` parameter can be used to access the captured and processed data frames
        from the calling code.
```



#### Advantages:

- Asynchronous packet capturing allows the main program to continue executing without waiting for packets to arrive, leading to better program responsiveness.
- Batch processing reduces processing overhead and allows handling large volumes of packets efficiently.
- Saving processed data frames as pickled files facilitates data persistence and easy data retrieval for analysis or further processing.

### Function load_dump_files

The load_dump_files function is responsible for loading and concatenating processed data frames from pickled files in the specified folder.

#### Here's what the function does

It reads all pickled files (.pkl) in the provided folder that have numeric filenames.
It concatenates the data frames from these files into a single pandas DataFrame.
The resulting DataFrame contains the concatenated data from the pickled files.

```python

    Load and concatenate processed data frames from pickled files in the specified folder.

    Args:
        folder (str): The folder path where the pickled data frames are stored.

    Returns:
        pd.DataFrame: A DataFrame containing the concatenated data from the pickled files.

    Note:
        This function reads all pickled files (*.pkl) in the specified folder that have numeric filenames.
        It concatenates the data frames from these files and returns a single DataFrame.

        The `folder` parameter should be the path to the folder containing the pickled files.
```




```python

from pdsniff import start_sniffing, load_dump_files
count = 1000
result_list = [] # results will be appended
killkey = "ctrl+alt+x"
folder_path="c:\\internetdump"
t2 = start_sniffing(
	count=count, result_list=result_list, killkey=killkey, dumpfolder=folder_path
)


df = load_dump_files(folder_path)

		
```