from pydub import AudioSegment
import random
from dir_helper import get_directory_structure
import logging, sys
import copy

def pick_songs (segments, bpm_offset_tolerance, songs_root_path, cross_time_ms = 5000, fade_time = 3000) :
    """ Picks the songs for the segments. These songs must have a length of at least seg1textTime+seg2textTime+exerciseTime+fadetime*3"""
    def get_song (required_time, bpm, n, song_dir_dict, travel, cross=False, cross_time = 5000) :
        sbpm = str(bpm)
        if not n : return ([], None)
        if not(sbpm in song_dir_dict) : return get_song (required_time, bpm+travel, n-1, song_dir_dict, travel, cross=cross, cross_time=cross_time)
        if not len(song_dir_dict[sbpm]) :
            return get_song (required_time, bpm+travel, n-1, song_dir_dict, travel, cross=cross, cross_time=cross_time)
        else :
            song = random.choice(list(song_dir_dict[sbpm].keys()))
            song_path = "./"+songs_root_path+"/"+sbpm+"/"+song
            song_audio = AudioSegment.from_mp3(song_path)

            if len(song_audio) > required_time :
                return ([song], sbpm)
            else :
                if (cross) :
                    del song_dir_dict[sbpm][song]
                    req_cross_songs = 1
                    songs = [song]
                    while len(song_audio) < required_time :
                        if len(song_dir_dict[sbpm]) < req_cross_songs :
                            return get_song (required_time, bpm+travel, n-1, song_dir_dict, travel, cross=True, cross_time=cross_time)
                        else :
                            cross_song = random.choice(list(song_dir_dict[sbpm].keys()))
                            del song_dir_dict[sbpm][cross_song]
                            songs.append(cross_song)
                            cross_song_path = "./"+songs_root_path+"/"+sbpm+"/"+cross_song
                            cross_song_audio = AudioSegment.from_mp3(cross_song_path)
                            song_audio = song_audio.append(cross_song_audio, crossfade=cross_time)
                    return (songs, sbpm)
                else :
                    del song_dir_dict[sbpm][song]
                    return get_song (required_time, bpm+travel, n-1, song_dir_dict, travel, cross=cross, cross_time=cross_time)

    songs_dir_dict = get_directory_structure(songs_root_path)[songs_root_path]

    for i in range(len(segments)) :
        print("Picking songs for segment " + str(i+1) + " of " + str(len(segments)))

        segment = segments[i]
        next_segment_text_time = len(segments[i+1].text_audio) if len(segments) > i+1 else 0
        req_fade_time = fade_time * 2 if i > 0 else fade_time * 3
        required_time = segment.get_exercise_duration_ms() + len(segment.text_audio) + next_segment_text_time + req_fade_time

        (songs, bpm) = get_song(required_time, segment.bpm, bpm_offset_tolerance, copy.deepcopy(songs_dir_dict), -1)
        if not len(songs) : (songs, bpm) = get_song(required_time, segment.bpm, bpm_offset_tolerance, copy.deepcopy(songs_dir_dict), +1)
        if not len(songs) : (songs, bpm) = get_song(required_time, segment.bpm, bpm_offset_tolerance, copy.deepcopy(songs_dir_dict), -1, cross=True, cross_time=cross_time_ms)
        if not len(songs) : (songs, bpm) = get_song(required_time, segment.bpm, bpm_offset_tolerance, copy.deepcopy(songs_dir_dict), +1, cross=True, cross_time=cross_time_ms)
        if not songs : raise Exception("Could either not find any song close enough to BPM: " + str(segment.bpm) + " or enough duration")

        logging.debug("Original BPM: " + str(segment.bpm))
        songs_audio = AudioSegment.from_mp3("./"+songs_root_path+"/"+bpm+"/"+songs[0])
        logging.info("Picked BPM " + str(bpm))
        logging.info("Picked song " + songs[0])
        del songs_dir_dict[bpm][songs[0]]

        for cross_song in songs[1:]:
            cross_song_audio = AudioSegment.from_mp3("./"+songs_root_path+"/"+bpm+"/"+cross_song)
            songs_audio = songs_audio.append(cross_song_audio, cross_time_ms)
            del songs_dir_dict[bpm][cross_song]
            logging.info("... crossed with song " + cross_song)

        segment.song_audio = songs_audio
