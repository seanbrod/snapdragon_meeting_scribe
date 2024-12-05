#capture input and processes data to text file

#use whisper AI and get lectures or videos to break down into text. 


#read in 5-10second audio chunks (mp3) files and process it with whisper then move onto the next chunk. will give the impression of real time transcription

# https://medium.com/@praveen.ponseeni/how-to-run-whisper-cpp-in-windows-a-step-by-step-guide-6bf900860d29  *possible solution

#make a stream of audio into the transcription

import whisper

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
#alternative: c++ implementation https://medium.com/@bhuwanmishra_59371/a-starter-guide-to-whisper-cpp-f238817fd876