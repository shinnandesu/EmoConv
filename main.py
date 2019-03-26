import pyaudio
import pandas as pd
from keras.models import load_model
from ubicoustics.vggish_input import waveform_to_examples, wavfile_to_examples
import os
import wget
from pathlib import Path
# Mymodels
import models
import EmoConv
import audios


    
def main(sem,scm,wav,pattern,reply,context):
    #detect emotion
    real_emotion = sem.detectSpeeechEmotion(wav)
    # Answer by Dialogflow
    ABD = models.AnswerModel()   
    answer,scenario_emotion = ABD.send_audio_request(wav)
    # Convert Emotion from Emotion and Context
    CVT = EmoConv.Converter(context,scenario_emotion)

    expression = CVT.convertEmotion(real_emotion,scm.predicted,pattern,reply)
    filename = "output/sorry.wav"
    if(answer!=""):
        # Text to Speech with Emotion 
        TTS = models.TTSModel()
        filename = TTS.getSpeechFile(answer,expression)
        # print ("tts_time:{}[sec]".format(time.time() - start_time))
    return filename

def check_dir():
    if not os.path.exists('output'):
        os.mkdir('output')
    if not os.path.exists('input'):
        os.mkdir('input')
    
if __name__ == "__main__":
    check_dir()
    myAudio = audios.AudioModel()
    MIC = myAudio.check_microphone()
    #load model
    MODEL_URL = "https://www.dropbox.com/s/cq1d7uqg0l28211/example_model.hdf5?dl=1"
    MODEL_PATH = "saved_models/Context_model.hdf5"
    model_filename = "saved_models/Context_Model.hdf5"
    ubicoustics_model = Path(MODEL_PATH)
    if (not ubicoustics_model.is_file()):
        print("Downloading Context_Model.hdf5 [867MB]: ")
        wget.download(MODEL_URL,MODEL_PATH)
    ContextModel = load_model(MODEL_PATH)
    EmotionModel = load_model("saved_models/Emotion_Model.h5")
    #create instance of the model
    SEM = models.SpeechEmotionModel(EmotionModel)
    SCM = models.SpeechContextModel(ContextModel)
    #clear the console
    clear = lambda: os.system('clear')
    clear()
    pattern = 0
    reply = 0
    context = int(input("Select the context (0:Home 1:Public 2:Alone 3:Group): "))
        
    while True:
        # recording the context by stream
        context_stream = myAudio.stream_record(SCM.audio_samples)
        context_stream.start_stream()
        while context_stream.is_active():
            try:
                print('=' * 70)
                pattern = int(input("Select the adaptation pattern (0:No 1:Random 2:Auto 3:Manual): "))
                print('=' * 70)
                if(pattern== 3):
                    reply = int(input("Select emotional reply you want (0:Neutral 1:Supportive 2:Happy 3:Sad 4:Angry): "))
                    print('=' * 70)
            except:
                continue

            if(reply<5 and pattern<4):
                ent = input('Please press the ENTER KEY to start recording! ')
                if(ent==""):
                    #stop recording the context
                    context_stream.stop_stream()
                     #start recording the voice
                    input_file = myAudio.voice_record()
                    #execute the main method
                    output_file = main(SEM,SCM,input_file,pattern,reply,context)
                    #play audio sounds
                    myAudio.playSound(output_file)
            else:
                continue