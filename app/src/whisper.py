#TODO: Part 1: save .wav of entire recording time. take input to start and stop. record entire time from start->stop
#               then transcibe this .wav using whipsper to get entire meeting transcription
#      Part 2: have real time audio transcription and recording to txt file. have gui make this stuff pop up. 
#      Part 3: save txt files top SQLite DB for later
#      Part 4: make gui to start and stop transcription. 
#      Part 5: use NPU for Whisper transcription
#      Part 6: add try catch exceptions and logging

# https://medium.com/@praveen.ponseeni/how-to-run-whisper-cpp-in-windows-a-step-by-step-guide-6bf900860d29  *possible solution

#alternative: c++ implementation https://medium.com/@bhuwanmishra_59371/a-starter-guide-to-whisper-cpp-f238817fd876
#https://github.com/openai/whisper/discussions/134 -onnx conversion of whisper
#https://github.com/ufal/whisper_streaming -chunking implemetation

#NPU
#https://docs.qualcomm.com/bundle/publicresource/topics/80-63442-50/introduction.html 
#https://www.qualcomm.com/developer/software/qualcomm-ai-engine-direct-sdk 

import whisper
import subprocess
import sounddevice as sd
import numpy as np
import wave

#TODO: make save txt to SQLlite DB function after finish
def save_to_db(files):
    print('y')

#TODO: make this transcribe the .wav file into a txt file. This will be the full meeting not chunks to be processed after program is done
def transcribe(file):
    model = whisper.load_model("medium.en")
    try:
        result = model.transcribe(file)
        output_path  = "process_data\\output_vid"
        with open(output_path+"\\output.txt", "w") as f:
            f.write(result["text"]+"\n")
        #print(result["text"])
    except Exception as e:
        print("Error", e)


#TODO: this is for the real time audio transciption during a meeting
def transcribe_chunk(chunk):
    with open("temp.wav", "wb") as f:
        f.write(chunk)
    result = subprocess.run(["whisper-cpp", "temp.wav", "--model", "path/to/model"], 
                             capture_output=True, text=True)
    return result.stdout

#TODO: test this to make sure it captures entire recording time of meeting
def record_system_audio(output_file="output.wav", record_seconds=10, sample_rate=44100, channels=2):
    """
    Records system audio (loopback) on Windows using WASAPI and saves it as a .wav file.

    :param output_file: Name of the output file (default: "output.wav").
    :param record_seconds: Duration of the recording in seconds (default: 10).
    :param sample_rate: Sample rate for recording (default: 44100 Hz).
    :param channels: Number of audio channels (default: 2 for stereo).
    """
    # Ensure WASAPI is used for loopback recording
    device_info = sd.query_devices(kind='output')
    loopback_device = sd.default.device = (None, device_info['index'])
    
    print(f"Using device: {device_info['name']}")

    print("Recording system audio...")
    audio_data = sd.rec(int(record_seconds * sample_rate), 
                        samplerate=sample_rate, 
                        channels=channels, 
                        dtype="int16", 
                        blocking=True)

    print("Recording complete.")

    # Save the recorded audio to a .wav file
    with wave.open(output_file, "wb") as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(2)  # 16-bit audio is 2 bytes per sample
        wf.setframerate(sample_rate)
        wf.writeframes(audio_data.tobytes())

    print(f"Audio saved to {output_file}")

#TODO: attached to chunks. test to see if works
def main():
    samplerate = 16000
    channels = 1

    with sd.InputStream(samplerate=samplerate, channels=channels, dtype="int16") as stream:
        while True:
            chunk, _ = stream.read(samplerate * 10)  # Read 10 seconds of audio
            text = transcribe_chunk(chunk.tobytes())
            print(text)
            
            
    # Example usage
    record_system_audio(output_file="system_audio.wav", record_seconds=10)

if __name__ == "__main__":
    main()
        