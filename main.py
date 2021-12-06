# %%
import streamlit as st
import csv

def load_data():
    csv_file = open("data/events.csv", encoding="utf-8")
    reader = csv.DictReader(csv_file)

    name_comment_dict = None
    id_record_dict = {}
    for line_no, record in enumerate(reader):
        if line_no == 0:
            name_comment_dict = record
        elif record["$id"] != "":
            id_record_dict[int(record["$id"])] = record
    return name_comment_dict, id_record_dict


name_comment_dict, id_record_dict = load_data()
min_id = min(id_record_dict.keys())
max_id = max(id_record_dict.keys())

st.sidebar.text(f"event id range: [{min_id}, {max_id}]")
evt_id = st.sidebar.number_input(label="event id", min_value=min_id, max_value=max_id, value=min_id, step=1)
record = id_record_dict[evt_id]
st.title("Life Restart Analysis")
for key, value in record.items():
    if value.strip() == "":
        continue
    elif key == "$id":
        st.header(value)
    else:
        st.text(f"{name_comment_dict[key]}: {value}")

# %%
