class Segment():
    def __init__(self, bpm, text, dur_min, dur_sec, comments):
        self.bpm = bpm
        self.text = text
        self.dur_min = dur_min
        self.dur_sec = dur_sec
        self.comments = comments
        self.text_audio = None
        self.song_audio = None
    
    def get_exercise_duration_ms (self) :
        return self.dur_min*60000 + self.dur_sec*1000