import json
import pyaudio
import wave
from keras.models import load_model
from sklearn.preprocessing import LabelEncoder
import numpy as np
import time
from ubicoustics.vggish_input import waveform_to_examples, wavfile_to_examples
import pyaudio
import os
# Mymodels
import models
import EmoCon 
import audios

    
def main(sem,scm,wav):
    start_time = time.time()
    #detect emotion
    emotion = sem.detectSpeeechEmotion(wav)
    # Answer by Dialogflow
    ABD = models.AnswerModel()   
    answer = ABD.send_audio_request(wav)
    # Convert Emotion from Emotion and Context
    CVT = EmoCon.Converter()
    expression = CVT.convertEmotion(emotion,scm.predicted)
    filename = "output/sorry.wav"
    if(answer!=""):
        # Text to Speech with Emotion 
        TTS = models.TTSModel()
        filename = TTS.getSpeechFile(answer,expression)
        print ("tts_time:{}[sec]".format(time.time() - start_time))
    return filename



if __name__ == "__main__":
    myAudio = audios.AudioModel()
    MIC = myAudio.check_microphone()
    #load model
    EmotionModel = load_model("models_file/Emotion_Voice_Detection_Model.h5")
    ContextModel = load_model("models_file/context_model.hdf5")
    #create instance of the model
    SEM = models.SpeechEmotionModel(EmotionModel)
    SCM = models.SpeechContextModel(ContextModel)
    #clear the console
    clear = lambda: os.system('clear')
    clear()
    while True:
        # recording the context by stream
        context_stream = myAudio.stream_record(SCM.audio_samples)
        context_stream.start_stream()
        while context_stream.is_active():
            print('='*40)
            s = input('Please push the ENTER KEY to start recording!')
            if(s==""):
                #stop recording the context
                context_stream.stop_stream()
                #start recording the voice
                input_file = myAudio.voice_record()
                #execute the main method
                output_file = main(SEM,SCM,input_file)
                #play audio sounds
                myAudio.playSound(output_file)
            else:
                continue
        



