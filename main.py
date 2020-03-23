import logging, sys
import configparser
from generator_code.json_parser import parse_json_segments
from generator_code.voices import generate_voices
from generator_code.generator import pick_songs
from generator_code.mp3_generator import generate_mp3

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
    config = configparser.ConfigParser()

    if len(sys.argv) > 1 :
        config.read(sys.argv[1])
    else :
        config.read('./default_settings.ini')

    program_path = config['settings']['Path_to_exercise_program_JSON']
    tempo_offset_threshold = int(config['settings']['Allowed_BPM_offset_if_no_song_for_particular_BPM_is_found'])
    fade_time_ms = int(config['settings']['Fade_time_in_MS'])
    songs_root_path = config['settings']['Path_to_root_of_songs_folder']
    speech_db_level = int(config['settings']['DB_Level_for_music_when_words_are_spoken'])
    comment_fade_in_out_time_ms = int(config['settings']['Fade_time_for_comments_in_MS'])

    main(program_path, songs_root_path, tempo_offset_threshold, fade_time_ms, speech_db_level, comment_fade_in_out_time_ms)