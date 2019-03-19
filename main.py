import pyaudio
from keras.models import load_model
from ubicoustics.vggish_input import waveform_to_examples, wavfile_to_examples
import os
import wget
from pathlib import Path
# Mymodels
import models
import EmoConv
import audios

    
def main(sem,scm,wav):
    start_time = time.time()
    #detect emotion
    emotion = sem.detectSpeeechEmotion(wav)
    # Answer by Dialogflow
    ABD = models.AnswerModel()   
    answer = ABD.send_audio_request(wav)
    # Convert Emotion from Emotion and Context
    CVT = EmoConv.Converter()
    expression = CVT.convertEmotion(emotion,scm.predicted)
    filename = "output/sorry.wav"
    # if(answer!=""):
    #     # Text to Speech with Emotion 
    #     TTS = models.TTSModel()
    #     filename = TTS.getSpeechFile(answer,expression)
    #     # print ("tts_time:{}[sec]".format(time.time() - start_time))
    return filename



if __name__ == "__main__":
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
        



