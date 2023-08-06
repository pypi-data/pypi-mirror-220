from scapy.all import *
from kthread_sleep import sleep
from kthread import KThread
from time import perf_counter_ns
import pandas as pd
from collections import deque
import keyboard
from tolerant_isinstance import isinstance_tolerant
from get_consecutive_filename import get_free_filename


def start_sniffing(
    count: int,
    result_list: None | list | deque = None,
    killkey: str = "ctrl+alt+x",
    dumpfolder: str | None = None,
    **kwargs,
) -> KThread:
    r"""
    Capture and process network packets asynchronously using Scapy library.

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

        Example usage:
        ```
        from pdsniff import start_sniffing
        from PrettyColorPrinter import add_printer
        add_printer(1)
        count = 1000
        result_list = []
        killkey = "ctrl+alt+x"
        t2 = start_sniffing(
            count=count, result_list=result_list, killkey=killkey, dumpfolder="c:\\internetdump"
        )

        ```
    """
    if isinstance_tolerant(result_list, None):
        result_list = deque([], 1)
    addtofile = 0
    if dumpfolder:
        if not os.path.exists(dumpfolder):
            os.makedirs(dumpfolder)
        addtofile = (
            int(
                get_free_filename(dumpfolder, fileextension=".pkl", leadingzeros=10)
                .split(os.sep)[-1]
                .split(".")[0]
            )
            - 1
        )
        if addtofile < 0:
            addtofile = 0
        addtofile = math.ceil(addtofile / count) * count

    def _get_frame():
        dafa = []
        isactive = True

        def add_to_dict(pref):
            st = str(key)
            g = pref + st
            if isinstance(item, list):
                wholedict[g] = tuple(item)
            else:
                wholedict[g] = item
            allkeys.add(g)

        def killme():
            nonlocal isactive
            isactive = False

        if killkey not in keyboard.__dict__["_hotkeys"]:
            keyboard.add_hotkey(killkey, killme)

        kwargs["prn"] = lambda x: dafa.append(x)
        if "count" in kwargs:
            del kwargs["count"]
        t = KThread(target=sniff, args=(), name=f"{perf_counter_ns()}", kwargs=kwargs)
        t.start()
        packnototal = 0

        while isactive:
            while len(dafa) <= count:
                if not isactive:
                    break
                sleep(0.1)

            dafa2 = []
            for _ in range(count):
                try:
                    dafa2.append(dafa.pop(0))
                except Exception as fe:
                    break
            if not dafa2:
                continue
            alldicts = []
            allkeys = set()
            for pq_q in enumerate(dafa2):
                pq, q = pq_q
                wholedict = {"pack_id": packnototal, "pack_time": q.time}
                packnototal += 1
                for key, item in q.fields.items():
                    add_to_dict("aa_")
                for key, item in q.payload.fields.items():
                    add_to_dict("bb_")

                for key, item in q.payload.payload.fields.items():
                    add_to_dict("cc_")

                for key, item in q.payload.payload.payload.fields.items():
                    add_to_dict("dd_")

                alldicts.append(wholedict)
            for _ in range(len(alldicts)):
                for a in allkeys - set(alldicts[_]):
                    if a.endswith("load"):
                        alldicts[_][a] = b""
                    elif a.endswith("options"):
                        alldicts[_][a] = ()

                    else:
                        alldicts[_][a] = pd.NA

            df = pd.DataFrame(alldicts).fillna(pd.NA)
            for col, dtype in dtypes.items():
                if col in df.columns:
                    try:
                        if df[col].dtype.name == dtype:
                            continue
                        df[col] = df[col].astype(dtype)
                    except Exception:
                        continue
            df = df.fillna(pd.NA)
            for col in df.columns:
                if col in dtypes:
                    continue
                try:
                    withoutdu = df[col].dropna().drop_duplicates()
                    if withoutdu.empty:
                        continue
                    if isinstance(withoutdu.iloc[0], int):
                        df[col] = df[col].astype("Int64")
                    elif isinstance(withoutdu.iloc[0], float):
                        df[col] = df[col].astype("Float64")
                    elif isinstance(withoutdu.iloc[0], str):
                        df[col] = df[col].astype("string")
                except Exception as fe:
                    continue

            if dumpfolder:
                pklfile = os.path.join(
                    dumpfolder, str(packnototal + addtofile).zfill(10) + ".pkl"
                )
                df.to_pickle(pklfile)
            result_list.append(df)
        try:
            t.kill()
        except Exception as fe:
            pass
        try:
            keyboard.remove_hotkey(killkey)
        except Exception as fe:
            pass

    t2 = KThread(target=_get_frame, name=f"{perf_counter_ns()}_")
    t2.start()
    return t2


def load_dump_files(folder):
    r"""
    Load and concatenate processed data frames from pickled files in the specified folder.

    Args:
        folder (str): The folder path where the pickled data frames are stored.

    Returns:
        pd.DataFrame: A DataFrame containing the concatenated data from the pickled files.

    Note:
        This function reads all pickled files (*.pkl) in the specified folder that have numeric filenames.
        It concatenates the data frames from these files and returns a single DataFrame.

        The `folder` parameter should be the path to the folder containing the pickled files.

        Example usage:
        ```
        folder_path = "c:\\internetdump"
        df = load_dump_files(folder_path)
        ```
    """
    return pd.concat(
        [
            pd.read_pickle(x)
            for x in glob(rf"{folder.rstrip(f'/{os.sep}')}/*.pkl")
            if re.match(r"\d{10}", x.split(os.sep)[-1].split(".")[0])
        ],
        ignore_index=True,
    ).fillna(pd.NA)


dtypes = {
    "pack_id": "uint32",
    "pack_time": "float64",
    "aa_dst": "string",
    "aa_src": "string",
    "aa_type": "uint32",
    "bb_options": "object",
    "bb_version": "Int64",
    "bb_ihl": "Int64",
    "bb_tos": "Int64",
    "bb_len": "Int64",
    "bb_id": "Int64",
    "bb_flags": "Int64",
    "bb_frag": "Int64",
    "bb_ttl": "Int64",
    "bb_proto": "Int64",
    "bb_chksum": "Int64",
    "bb_src": "string",
    "bb_dst": "string",
    "cc_sport": "Int64",
    "cc_dport": "Int64",
    "cc_len": "Int64",
    "cc_chksum": "Int64",
    "dd_load": "object",
    "cc_window": "Int64",
    "cc_type": "Int64",
    "cc_reserved": "Int64",
    "cc_unused": "object",
    "cc_id": "Int64",
    "cc_urgptr": "Int64",
    "cc_dataofs": "Int64",
    "cc_ack": "Int64",
    "cc_flags": "string",
    "cc_code": "Int64",
    "cc_options": "object",
    "cc_seq": "Int64",
    "dd_ad": "Int64",
    "dd_an": "string",
    "dd_ra": "Int64",
    "dd_nscount": "Int64",
    "dd_ns": "string",
    "dd_id": "Int64",
    "dd_cd": "Int64",
    "dd_aa": "Int64",
    "dd_tc": "Int64",
    "dd_qdcount": "Int64",
    "dd_arcount": "Int64",
    "dd_rd": "Int64",
    "dd_qd": "string",
    "dd_qr": "Int64",
    "dd_opcode": "Int64",
    "dd_ancount": "Int64",
    "dd_rcode": "Int64",
    "dd_z": "Int64",
    "cc_length": "Int64",
    "dd_ihl": "Int64",
    "dd_tos": "Int64",
    "dd_len": "Int64",
    "dd_flags": "object",
    "dd_dst": "string",
    "dd_frag": "Int64",
    "dd_ttl": "Int64",
    "dd_options": "object",
    "dd_chksum": "Int64",
    "cc_nexthopmtu": "Int64",
    "dd_src": "string",
    "dd_proto": "Int64",
    "dd_version": "Int64",
    "bb_load": "object",
    "bb_hlim": "Int64",
    "bb_tc": "Int64",
    "cc_cksum": "Int64",
    "dd_type": "Int64",
    "cc_tgt": "string",
    "bb_nh": "Int64",
    "bb_fl": "Int64",
    "cc_res": "Int64",
    "dd_lladdr": "string",
    "bb_plen": "Int64",
    "dd_SUFFIX1": "Int64",
    "dd_NULL1": "Int64",
    "dd_SourceIP": "string",
    "dd_DestinationName": "string",
    "dd_SUFFIX2": "Int64",
    "dd_Offset": "Int64",
    "dd_Length": "Int64",
    "dd_Flags": "Int64",
    "dd_ID": "Int64",
    "dd_SourceName": "string",
    "dd_Type": "Int64",
    "dd_NULL2": "Int64",
    "dd_SourcePort": "Int64",
}
