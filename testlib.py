from gtts import gTTS

def speak(st):
    tts = gTTS(text=st, lang="en")
    filename = "/media/test.mp3"
    tts.save(filename)

speak("혼저옵서예")