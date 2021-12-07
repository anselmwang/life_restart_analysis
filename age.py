# %%
import json
from dataclasses import dataclass
import os
from typing import Dict, List
import logging

logging.basicConfig(format='%(asctime)s %(name)s:%(levelname)s:%(message)s', level=logging.INFO)
logger = logging.getLogger(os.path.basename(__file__))

@dataclass
class AgeEventRecord:
    event_id : int
    weight : float

@dataclass
class AgeRecord:
    age: int
    events: List[AgeEventRecord]

class AgeData:
    def __init__(self):
        raw_age_data = json.load(open('data/age.json', encoding="utf-8"))
        age_records = []
        for value in raw_age_data.values():
            age = int(value["age"])
            events = []
            seen_event_id_set = set()
            for item in value["event"]:
                if isinstance(item, int):
                    age_event_record = AgeEventRecord(item, 1)
                else:
                    assert isinstance(item, str)
                    if "*" not in item:
                        age_event_record = AgeEventRecord(int(item), 1)
                    else:
                        segs = item.split("*")
                        if len(segs) > 2:
                            logger.warn(f"Meet invalid aget event record {item}")
                            continue
                        age_event_record = AgeEventRecord(int(segs[0]), float(segs[1]))
                # there are duplication in input data
                if age_event_record.event_id not in seen_event_id_set:
                    seen_event_id_set.add(age_event_record.event_id)
                    events.append(age_event_record)
            age_records.append(AgeRecord(age, events))
            


        self._age_records = age_records
        self._age_dict = {}
        for age_record in self._age_records:
            self._age_dict[age_record.age] = age_record


    def get_age_list(self):
        age_list = [age_record.age for age_record in self._age_records]
        age_list.sort()
        return age_list

        
    def get(self, age: int) -> AgeRecord:
        return self._age_dict[age]
