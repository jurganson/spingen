import logging, sys
from json_parser import parse_json_segments
from voices import generate_voices
from generator import pick_songs
from mp3_generator import generate_mp3

logging.basicConfig(stream=sys.stderr, level=logging.FATAL)

def main (program_path = "./program_examples/dummy_program.json", 
          songs_root_path = "./songs", 
          tempo_offset_threshold = 11, 
          fade_time_ms = 3000, 
          speech_db_level = 20, 
          comment_fade_in_out_time_ms = 500) :

    segments = parse_json_segments(program_path)
    
    generate_voices(segments)
    pick_songs(segments, tempo_offset_threshold, songs_root_path)
    generate_mp3(segments, fade_time_ms, speech_db_level, comment_fade_in_out_time_ms)

if __name__ == "__main__":
    main()