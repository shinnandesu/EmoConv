import numpy as np
import pandas as pd
import json
from os.path import join, dirname
from watson_developer_cloud import TextToSpeechV1
import threading
import dialogflow_v2 as dialogflow
import uuid
import tensorflow as tf
import pyaudio
import librosa
from ubicoustics import vggish_params
from ubicoustics.vggish_input import waveform_to_examples, wavfile_to_examples
import time
import config

class SpeechEmotionModel:
    def __init__(self,model):
        self.model = model
        
    def detectSpeeechEmotion(self,wav):
        X, sample_rate = librosa.load(wav, res_type='kaiser_fast')
        print(sample_rate)
        mfccs = np.mean(librosa.feature.mfcc(y=X, sr=sample_rate, n_mfcc=40).T,axis=0) 
        livedf2= pd.DataFrame(data=mfccs)
        livedf2 = livedf2.stack().to_frame().T
        twodim= np.expand_dims(livedf2, axis=2)
        livepreds = self.model.predict(twodim, batch_size=16,verbose=1)
        livepreds1=livepreds.argmax(axis=1)
        liveabc = livepreds1.astype(int).flatten()
        return liveabc[0]

class SpeechContextModel:
    def __init__(self,model):
        self.model = model
        self.graph = tf.get_default_graph()
        self.predicted = []

    def audio_samples(self,in_data, frame_count, time_info, status_flags):
        np_wav = np.fromstring(in_data, dtype=np.int16) / 32768.0 # Convert to [-1.0, +1.0]
        x = waveform_to_examples(np_wav, 16000)
        predictions = []
        with self.graph.as_default():
            if x.shape[0] != 0:
                x = x.reshape(len(x), 96, 64, 1)
                pred = self.model.predict(x)
                predictions.append(pred)
            for prediction in predictions:
                m = np.argmax(prediction[0])
                if(float(prediction[0,m])>0.5):
                    self.predicted.append(m)
        return (in_data, pyaudio.paContinue)


    def detectSpeeechContext(self,wav):
        x = wavfile_to_examples(wav)
        x = x.reshape(len(x), 96, 64, 1)
        predictions = self.model.predict(x)
        predicted = []
        for k in range(len(predictions)):
            prediction = predictions[k]
            m = np.argmax(prediction)
            predicted.append(m)
        return predicted

class AnswerModel: 
    project_id = config.g_project_id
    client_access_token = config.g_client_access_token 
    language_code = 'en'
    audio_encoding = dialogflow.enums.AudioEncoding.AUDIO_ENCODING_LINEAR_16
    sample_rate_hertz = 16000 
    session_client = dialogflow.SessionsClient()
    session_id = uuid.uuid4().hex
    session = session_client.session_path(project_id, session_id)
    # Note: hard coding audio_encoding and sample_rate_hertz for simplicity.
    
    def send_audio_request(self,path):

        session = self.session_client.session_path(self.project_id, self.session_id)
        # print('Session path: {}\n'.format(session))
        with open(path, 'rb') as audio_file:
            input_audio = audio_file.read()

        audio_config = dialogflow.types.InputAudioConfig(
            audio_encoding=self.audio_encoding, language_code=self.language_code,
            sample_rate_hertz=self.sample_rate_hertz)
        query_input = dialogflow.types.QueryInput(audio_config=audio_config)
        response = self.session_client.detect_intent(
            session=session, query_input=query_input,
            input_audio=input_audio)
        print('=' * 40)
        print('Query text: {}'.format(response.query_result.query_text))
        # print('Detected intent: {} (confidence: {})\n'.format(
        #     response.query_result.intent.display_name,
        #     response.query_result.intent_detection_confidence))
        answer = response.query_result.fulfillment_text
        print('Fulfillment text: {}\n'.format(answer))

        return answer

class TTSModel:
    key = config.tts_key
    url = "https://gateway-lon.watsonplatform.net/text-to-speech/api"

    def getSpeechFile(self,t,e):
        output_wav = "./output/output-{}.wav".format(time.strftime("%Y%m%d-%H%M%S"))
        SSML = '<express-as type="{}">{}</express-as>'.format(e,t)
        tts = TextToSpeechV1(iam_apikey=self.key,url= self.url)
        # result = tts.list_voices().get_result()
        with open(output_wav,'wb') as audio_file:
            response = tts.synthesize(
                SSML,
                accept='audio/wav',
                voice="en-US_AllisonVoice"
            ).get_result()
            audio_file.write(response.content)
        # pronunciation = tts.get_pronunciation('Watson', format='spr').get_result()
        return output_wav