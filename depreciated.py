

    """

    if "what is the capital of" in data or "what's the capital of" in data or "what is the capital city of" in data or "what's the capital city of" in data:
        raw_data = data
        data = data.split(" ")
        print(data)
        search = ""
        if "what is the capital of" in raw_data:
            for word in data[5:]:
                search = search + word + " "
        elif "what's the capital of" in raw_data:
            for word in data[4:]:
                search = search + word + " "
        elif "what is the capital city of" in raw_data:
            for word in data[6:]:
                search = search + word + " "
        elif "what's the capital city of" in raw_data:
            for word in data[5:]:
                search = search + word + " "
        search = search[:len(search)-1]
        print(search)
        country_csv = open('country-list.csv', 'r')
        countries = csv.reader(country_csv)
        capital = ""
        for row in countries:
            if row[0].lower() == search:
                capital = row[1]
                break
        if capital != "":
            speak("The capital of " + search + " is " + capital)
        else:
            speak("I do not know what the capital of " + search + " is")
        country_csv.close()
"""
"""
#Set up audio capture
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
CHUNK = 1024
RECORD_SECONDS = 3
WAVE_OUTPUT_FILENAME = "buffer.wav"

audio = pyaudio.PyAudio()

stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
print("Audio is being recorded...")
frames = []

for i in range(0, int(RATE/CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data)
print("Recording done")

waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
waveFile.setnchannels(CHANNELS)
waveFile.setsampwidth(audio.get_sample_size(FORMAT))
waveFile.setframerate(RATE)
waveFile.writeframes(b''.join(frames))
waveFile.close()
"""
