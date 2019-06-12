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
import time
import tkinter

label_text = ""

def main(sem,scm,wav,pattern,reply,context,myAudio):
    #detect emotion
    real_emotion = sem.detectSpeeechEmotion(wav)
    start_time = time.time() 
    # Answer by Dialogflow
    ABD = models.AnswerModel()   
    answer,scenario_emotion = ABD.send_audio_request(wav)
    # Convert Emotion from Emotion and Context
    CVT = EmoConv.Converter(context,scenario_emotion)
    print ("createanswer_time:{}[sec]".format(time.time() - start_time))

    expression = CVT.convertEmotion(real_emotion,scm.predicted,pattern,reply)
    filename = "output/sorry.wav"
    if(answer!=""):
        # Text to Speech with Emotion 
        TTS = models.TTSModel()
        filename = TTS.getSpeechFile(answer,expression)
        print ("tts_time:{}[sec]".format(time.time() - start_time))

    myAudio.playSound(filename)
    return filename

def check_dir():
    if not os.path.exists('output'):
        os.mkdir('output')
    if not os.path.exists('input'):
        os.mkdir('input')
def click_btn(SEM,SCM,pattern,reply,context,myAudio):
    # button_clicked = True
    print("clicked")
    tekisuto["text"] = "recording 5sec..."
    input_file = myAudio.voice_record()
    tekisuto["text"] = "finish"

    #execute the main method
    main(SEM,SCM,input_file,pattern,reply,context,myAudio)

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
    pattern = 2
    reply = 0
    context = 0
    
    root = tkinter.Tk()
    root.title(u"Software Title")
    root.geometry("400x300")
    #ボタン
    Button = tkinter.Button(text='Start Recording',command=lambda:click_btn(SEM,SCM,pattern,reply,context,myAudio))
    Button.pack()
    Button.place(x=10,y=30)

    tekisuto = tkinter.Label(text=label_text)
    tekisuto.place(x=150, y=5)

    root.mainloop() 
    # context_stream = myAudio.stream_record(SCM.audio_samples)
    # context_stream.start_stream()
    # while context_stream.is_active():
        # print("hoge")
        # if button_clicked == True: 
            #stop recording the context
            # context_stream.stop_stream()
            # input_file = myAudio.voice_record()
            #execute the main method
            # main(SEM,SCM,input_file,pattern,reply,context,myAudio)
            # button_clicked = False
            #play audio sounds
        # else:
        #     continue
