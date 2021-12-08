# %%
import csv
from dataclasses import dataclass
from typing import Dict, List, Optional
import os
import logging
import re

logging.basicConfig(format='%(asctime)s %(name)s:%(levelname)s:%(message)s', level=logging.INFO)
logger = logging.getLogger(os.path.basename(__file__))

EVT_COND_RE = re.compile(r"EVT\?\[(((\d+),?)+)\]")
@dataclass
class EventRecord:
    event_id: int
    event: str
    post_event: str
    effect_dict: Dict
    include: str
    exclude: str
    branches: List[str]
    others: Dict

    @staticmethod
    def extract_event_ids_from_cond(s: str) -> List[int]:
        """s = "EVT?[10026,10030]"""
        event_ids = []
        for m in EVT_COND_RE.finditer(s):
            if m is not None:
                event_ids.extend([int(x) for x in m.group(1).split(",")])
        # avoid potential duplication 
        event_ids = list(dict.fromkeys(event_ids))
        return event_ids

    @staticmethod 
    def extract_event_id_from_branch(branch_s: str) -> int:
        """TLT?[1002]:10006"""
        assert ":" in branch_s
        return int(branch_s.rsplit(":", 1)[1])

    
class EventData:
    def __init__(self):
        csv_file = open("data/events.csv", encoding="utf-8")
        reader = csv.DictReader(csv_file)

        # name_comment_dict = None
        # id_record_dict = {}
        # for line_no, record in enumerate(reader):
        #     if line_no == 0:
        #         name_comment_dict = record
        #     elif record["$id"] != "":
        #         id_record_dict[int(record["$id"])] = record
        
        event_records: List[EventRecord] = []
        for line_no, record in enumerate(reader):
            if line_no == 0:
                continue
            elif record["$id"] != "":
                event = record["event"].strip()
                assert event != ""
                post_event = record["postEvent"]
                if post_event.strip() == "":
                    post_event = None
                event_dict = {key:value for key, value in record.items() if key.startswith("effect:") and value.strip() != ""}
                include = record["include"].strip() if record["include"].strip() !=  "" else None
                exclude = record["exclude"].strip() if record["exclude"].strip() !=  "" else None
                branches = []
                for key in ("branch[0]", "branch[1]", "branch[2]"):
                    branch_str = record[key].strip()
                    if branch_str != "":
                        branches.append(branch_str)
                others = {}
                for key, value in record.items():
                    if key in ("$id", "event", "postEvent", "include", "exclude"):
                        continue
                    if key.startswith("branch[") or key.startswith("effect:"):
                        continue
                    others[key] = value
                event_records.append(EventRecord(
                    event_id=int(record["$id"]),
                    event=event,
                    post_event=post_event,
                    effect_dict= event_dict,
                    include=include,
                    exclude=exclude,
                    branches=branches,
                    others=others
                ))
        
        self._event_records = event_records
        self._event_dict = {event_record.event_id: event_record for event_record in event_records}


    def get(self, event_id:int) -> Optional[EventRecord]:
        return self._event_dict.get(event_id, None)


# %%
