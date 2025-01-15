#Sean Broderick
import pyaudio, wave, tempfile, subprocess, os


#DOCS
# https://medium.com/microsoftazure/build-and-deploy-fast-and-portable-speech-recognition-applications-with-onnx-runtime-and-whisper-5bf0969dd56b run whisper with onnx runtime and whisper onnx export

def transcribe_to_txt(input_filename: str, output_filename: str):
    print("Running Whisper transcription...")
    # Compose the command for Whisper
    command = ['./main', '-f', input_filename, '-otxt', '-of', output_filename, '-np']

    # Execute the command and capture output
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode != 0:
        print("Error during transcription:", result.stderr)
    else:
        print("Transcription completed.")

def capture_audio(self): #TODO: save entire transcription to textfile as well as sending out tokens to main
    # Initialize PyAudio
    p = pyaudio.PyAudio()

    # Find the default loopback device for system audio capture
    for i in range(p.get_device_count()):
        device_info = p.get_device_info_by_index(i)
        if device_info.get("name") == "Stereo Mix" or device_info.get("hostApi") == "Windows WASAPI" and device_info.get(
                "maxInputChannels") > 0:
            loopback_device_index = i
            break
    else:
        print("Could not find a loopback device for system audio capture.")
        return

    print(f"Using device: {p.get_device_info_by_index(loopback_device_index).get('name')}")

    # Set up stream for capturing system audio
    stream = p.open(format=pyaudio.paInt16,  # 16-bit audio
                    channels=2,  # Stereo
                    rate=44100,  # CD quality
                    input=True,
                    frames_per_buffer=44100 * 5,  # 5 seconds of audio
                    input_device_index=loopback_device_index,
                    as_loopback=True)

    try:
        print("Recording system audio... Press Ctrl+C to stop.")
        while True:
            # Read audio data from the stream
            audio_data = stream.read(44100 * 5, exception_on_overflow=False)

            # Save audio data to a temporary WAV file
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav", prefix="system_audio_", dir=".") as tmpfile:
                with wave.open(tmpfile.name, "wb") as wav_file:
                    wav_file.setnchannels(2)  # Stereo
                    wav_file.setsampwidth(p.get_sample_size(pyaudio.paInt16))
                    wav_file.setframerate(44100)
                    wav_file.writeframes(audio_data)

                # Transcribe the saved audio
                output_filename = tmpfile.name.replace(".wav", "")
                transcribe_to_txt(tmpfile.name, output_filename)

                # Print the transcribed text
                try:
                    with open(output_filename + ".txt", "r") as file:
                        print(file.read())
                except FileNotFoundError:
                    print("Transcription output not found.")

                # Clean up temporary files
                os.remove(tmpfile.name)
                if os.path.exists(output_filename + ".txt"):
                    os.remove(output_filename + ".txt")
    except KeyboardInterrupt:
        print("Recording stopped.")
    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()

if __name__ == "__main__":
    capture_audio()
