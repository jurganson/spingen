from gtts import gTTS as ttos
from pydub import AudioSegment
import os

def generate_mp3 (segments, fade_ms, speech_gain, comment_fade_ms, language = "en", output_file_name = "generated_program_sound") :
    def apply_comments (exercise_audio, segment) :
        new_exercise_audio = exercise_audio

        for comment in segment.comments :
            comment_audio = comment["comment_audio"]
            comment_time_ms = comment["second"]*1000 + comment["minute"]*60000
            part_01 = new_exercise_audio[comment_time_ms:comment_time_ms+len(comment_audio)+comment_fade_ms*2]
            part_02 = part_01.fade(to_gain=-speech_gain, start=0, end=comment_fade_ms)
            part_02 = part_02.fade(to_gain= speech_gain, start=comment_fade_ms+len(comment_audio), end=len(part_02))
            part_02 = part_02.overlay(comment_audio, position=comment_fade_ms)
            new_exercise_audio = new_exercise_audio[:comment_time_ms] + part_02 + new_exercise_audio[comment_time_ms+len(part_02):] 

        return new_exercise_audio

    def append_segment (current_audio, next_segment, future_segment) :
        segment_audio = next_segment.song_audio
        segment_audio_faded = segment_audio - speech_gain
        segment_text_audio = next_segment.text_audio

        part_01 = segment_audio_faded[:len(segment_text_audio)] # First part of next segment
        part_01 = current_audio[-len(segment_text_audio):].append(part_01, crossfade=len(segment_text_audio)).overlay(segment_text_audio) # 
        
        part_02 = part_01 + segment_audio_faded[len(part_01):len(part_01)+fade_ms].fade(to_gain=speech_gain, start=0, end=fade_ms) # Faded up to exercise gain
        part_03 =           apply_comments(segment_audio[len(part_02):len(part_02)+next_segment.get_exercise_duration_ms()+fade_ms], next_segment) # Apply comments to exercise
        part_03 = part_02 + part_03.fade(to_gain=-speech_gain, start=len(part_03)-fade_ms, end=len(part_03))
        part_04 = current_audio[:-len(segment_text_audio)] + part_03

        if not future_segment :
            part_05 = part_04.fade_out(fade_ms)
            ttos(text="Program finished", lang=language, slow=False).save("output.mp3")
            finish_voice = AudioSegment.from_file("output.mp3")
            print("Cleaning up output.mp3")
            os.remove("output.mp3")
            return part_05 + finish_voice
        else :
            part_05 = part_04 + segment_audio_faded[len(part_03):len(part_03)+len(future_segment.text_audio)]
            return part_05

    print("Generating MP3 for segment 1 of " + str(len(segments)))

    intro_segment_audio = segments[0].song_audio
    intro_segment_text_audio = segments[0].text_audio
    intro_segment_audio_faded = intro_segment_audio - speech_gain

    part_01 = intro_segment_audio_faded[:fade_ms].fade_in(fade_ms)
    part_02 = part_01 + intro_segment_audio_faded[len(part_01):len(part_01)+len(intro_segment_text_audio)].overlay(intro_segment_text_audio)
    part_03 = part_02 + intro_segment_audio_faded[len(part_02):len(part_02)+fade_ms].fade(to_gain=speech_gain, start=0, end=fade_ms)
    part_04 =           apply_comments(intro_segment_audio[len(part_03):len(part_03)+segments[0].get_exercise_duration_ms()+fade_ms], segments[0])
    part_04 = part_03 + part_04.fade(to_gain=-speech_gain, start=len(part_04)-fade_ms, end=len(part_04))
    part_05 = part_04 + intro_segment_audio_faded[len(part_04):len(part_04)+len(segments[1].text_audio)]

    program_audio = part_05

    for i in range(1, len(segments)) :
        print("Generating MP3 for segment " + str(i+1) + " of " + str(len(segments)))

        if i+1 >= len(segments) :
            program_audio = append_segment(program_audio, segments[i], None)
        else :
            program_audio = append_segment(program_audio, segments[i], segments[i+1])

    
    if not os.path.exists("./output") :
        os.mkdir("./output")

    print("Exporting final mp3 ...")
    file_path = "./output/"+output_file_name+".mp3"
    program_audio.export(file_path, format="mp3")
    print("Done! Exported mp3 to "+ file_path)
