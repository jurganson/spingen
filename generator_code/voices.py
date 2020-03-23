from gtts import gTTS as ttos
from pydub import AudioSegment
import os

def generate_voices (segments, language = "en") :
    count = 1
    for segment in segments :
        print("Generating voices for segment " + str(count) + " of " + str(len(segments)))
        count += 1
        output = ttos(text=segment.text, lang=language, slow=False)
        output.save("output.mp3")
        speech_sound = AudioSegment.from_file("output.mp3")
        segment.text_audio = speech_sound

        for comment in segment.comments :
            output = ttos(text=comment["comment"], lang=language, slow=False)
            output.save("output.mp3")
            speech_sound = AudioSegment.from_file("output.mp3")
            comment["comment_audio"] = speech_sound

    print("Cleaning up output.mp3")
    os.remove("output.mp3")