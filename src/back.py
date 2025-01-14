import qai_hub as hub

#devices = hub.get_devices()
#print(devices)

#use whisper AI and get lectures or videos to break down into text. 
#https://medium.com/@jwcsavage/using-openais-whisper-to-transcribe-real-time-audio-c2ea27f6037f 5 sec breakup

#FUNCTIONS___________________________________________________________________________________________

def transcribe_to_txt(input_filename: str, output_filename: str):
    print('Running whisper transcription...')
    # Compose the command of all components
    command = ['./main', '-f', input_filename, '-otxt', '-of', output_filename, '-np']

    # Execute the command
    result = subprocess.run(command, capture_output=True, text=True)

def test_function():
    transcribe_to_txt('audio_xkf1lhwh.wav', 'output.txt')

def callback(indata, frames, time, status):
    # Raise for status if required
    if status:
        print(status)
    
    # Create a tempfile to save the audio to, with autodeletion
    with tempfile.NamedTemporaryFile(delete=True, suffix='.wav', prefix='audio_', dir='.') as tmpfile:
        # Save the 5 second audio to a .wav file
        with wave.open(tmpfile.name, 'wb') as wav_file:
            wav_file.setnchannels(1)  # Mono audio
            wav_file.setsampwidth(2)  # 16-bit audio
            wav_file.setframerate(16000)  # Sample rate
            wav_file.writeframes(indata)
        
        # Prepare the output filename
        output_filename = tmpfile.name.replace('.wav', '')
        
        # Transcribe the audio to text using our whisper.cpp wrapper
        transcribe_to_txt(tmpfile.name, output_filename)

        # Print the transcribed text
        with open(output_filename + '.txt', 'r') as file:
            print(file.read())
        
        # Clean up temporary files
        os.remove(output_filename + '.txt')

def run():
    try:
        # Start recording with a rolling 5-second buffer
        with sd.InputStream(callback=callback, dtype='int16', channels=1, samplerate=16000, blocksize=16000*5):
            print("Recording... Press Ctrl+C to stop.")
            while True:
                pass
    except KeyboardInterrupt:
        print('Recording stopped.')

#MAIN___________________________________________________________________________________________

def main():
    execution_time = timeit.timeit('test_function()', globals=globals(), number=100)
    print(f"Average execution time: {execution_time / 100:.5f} seconds")    

if __name__ == "__main__":
    main()