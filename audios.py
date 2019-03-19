import pyaudio
import wave
import time
from ubicoustics import microphones
import argparse

class AudioModel:
    # Variables
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000
    CHUNK = RATE
    MICROPHONES_DESCRIPTION = []
    FPS = 60.0
    SECONDS = 5 
    MICROPHONE_INDEX = 0

    def check_microphone(self):
        print("1 / 2: Checking Microphones... ")
        print("="*40)

        desc, mics, indices = microphones.list_microphones()
        if (len(mics) == 0):
            print("Error: No microphone found.")
            exit()

        #############
        # Read Command Line Args
        #############
        parser = argparse.ArgumentParser()
        parser.add_argument("-m", "--mic", help="Select which microphone / input device to use")
        args = parser.parse_args()
        try:
            if args.mic:
                self.MICROPHONE_INDEX = int(args.mic)
                print("User selected mic: %d" % self.MICROPHONE_INDEX)
            else:
                mic_in = input("Select microphone [%d]: " % self.MICROPHONE_INDEX).strip()
                if (mic_in!=''):
                    self.MICROPHONE_INDEX = int(mic_in)
        except:
            print("Invalid microphone")
            exit()
        # Find description that matches the mic index
        mic_desc = ""
        for k in range(len(indices)):
            i = indices[k]
            if (i==self.MICROPHONE_INDEX):
                mic_desc = mics[k]
        print("Using mic: %s" % mic_desc)
        

    def stream_record(self,callback):
        p = pyaudio.PyAudio()
        stream = p.open(format=self.FORMAT, channels=self.CHANNELS, rate=self.RATE, input=True, frames_per_buffer=self.CHUNK, stream_callback=callback, input_device_index=self.MICROPHONE_INDEX)

        return stream

    def voice_record(self):
        p = pyaudio.PyAudio()
        stream = p.open(format=self.FORMAT, channels=self.CHANNELS,rate=self.RATE, input=True,input_device_index = self.MICROPHONE_INDEX, frames_per_buffer=self.CHUNK)
        frames = []
        print("~"*40)                
        print ("recording for 5 sec...")
        print("~"*40)                
        for i in range(0, int(self.RATE / self.CHUNK * self.SECONDS)):
            data = stream.read(self.CHUNK)
            frames.append(data)
        print ("finished recording")
        print("="*40)                
        stream.stop_stream()
        stream.close()
        p.terminate()
        input_wav = "./input/input-{}.wav".format(time.strftime("%Y%m%d-%H%M%S"))
        waveFile = wave.open(input_wav, 'wb')
        waveFile.setnchannels(self.CHANNELS)
        waveFile.setsampwidth(p.get_sample_size(self.FORMAT))
        waveFile.setframerate(self.RATE)
        waveFile.writeframes(b''.join(frames))
        waveFile.close()

        return input_wav
        
    def playSound(self,wav):
        try:
            wf = wave.open(wav, "r")
        except FileNotFoundError: #not existing file
            print("[Error 404] No such file or directory: " + wav)
            return 0
                
        # open stream 
        p = pyaudio.PyAudio()
        wf = wave.open(wav, "r")
        stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),channels=wf.getnchannels(),rate=wf.getframerate(),output=True)
        data = wf.readframes(self.CHUNK)
        a = 0
        while a<=200000:
            a+=1
            stream.write(data)
            data = wf.readframes(self.CHUNK)
        p.terminate()

