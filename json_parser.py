import json
from segment import Segment

def parse_json_segments (filename) :
    segments = []

    with open(filename, 'r') as f:
        spin_dict = json.load(f)

    for segment in spin_dict:
        seg_obj = Segment(
            segment["bpm"],
            segment["text"],
            segment["duration_minute"],
            segment["duration_second"],
            segment["comments"]
        )
        segments.append(seg_obj)

    return segments