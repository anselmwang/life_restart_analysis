import streamlit as st
import csv

import age
import event
def local_css(file_name):
    with open(file_name) as f:
        st.markdown('<style>{}</style>'.format(f.read()), unsafe_allow_html=True)

local_css("style.css")

def _show_event(event_record: event.EventRecord, event_data: event.EventData, ui_path="", ignore_basic=False):
    if not ignore_basic:
        st.write(f"event_id: {event_record.event_id}")
        st.write(f"event: {event_record.event}")
    if event_record.post_event is not None:
        st.write(f"post_event: {event_record.post_event}")
    if len(event_record.effect_dict) != 0:
        st.write(f"effect_dict: {event_record.effect_dict}")
    if event_record.include is not None:
        st.write(f"include: {event_record.include}")
        ext_event_ids = event.EventRecord.extract_event_ids_from_cond(event_record.include)
        for ext_event_id in ext_event_ids:
            show_event(event_data, ext_event_id, parent_ui_path=ui_path+"/include")
    if event_record.exclude is not None:
        st.write(f"exclude: {event_record.exclude}")
        ext_event_ids = event.EventRecord.extract_event_ids_from_cond(event_record.exclude)
        for ext_event_id in ext_event_ids:
            show_event(event_data, ext_event_id, parent_ui_path=ui_path+"/exlcude")
    if len(event_record.branches) != 0:
        st.write(f"branches: {event_record.branches}")
        for branch in event_record.branches:
            ext_event_ids = event.EventRecord.extract_event_ids_from_cond(branch)
            for ext_event_id in ext_event_ids:
                show_event(event_data, ext_event_id, parent_ui_path=ui_path+"/branch_cond")
            ext_event_id = event.EventRecord.extract_event_id_from_branch(branch)
            show_event(event_data, ext_event_id, parent_ui_path=ui_path+"/branch")
        
    if len(event_record.others) != 0:
        st.write(f"others: {event_record.others}")

def show_event(event_data: event.EventData, event_id: int, parent_ui_path=""):
    event_record = event_data.get(event_id)
    if event_record is not None:
        ui_path = parent_ui_path + f"/{event_id}"
        if st.checkbox(f"{event_id}_{event_record.event}*{age_event_record.weight}", key=ui_path):
            with st.container():
                _show_event(event_record, event_data, ui_path, True)


age_data = age.AgeData()
# selected_age = st.sidebar.selectbox("Age:", age_data.get_age_list())
selected_age = st.sidebar.number_input("age", min_value=0, max_value=110, value=0, step=1)

age_record = age_data.get(selected_age)

event_data = event.EventData()

# # %%
for age_event_record in age_record.events:
    event_id = age_event_record.event_id
    show_event(event_data, event_id)
    