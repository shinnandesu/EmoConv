# EmoConv
## Using
- [Dialogflow API](https://dialogflow.com/)
- [IBM Watson Text to Speech API](https://text-to-speech-demo.ng.bluemix.net/)
- [Ubicoustics Model](https://github.com/figlab/ubicoustics)

# System Requirements
The system is written in `python3`.

```bash
$ pip install -r requirement.txt 
```

# Setting
Create `config.py` file.
```bash
$ touch config.py
```
Edit `config.py` on your keys.
```python
g_project_id = 'xxxxxxxx' #Google Cloud Platform project ID 
g_client_access_token = 'xxxxxxxx' #Google Cloud Platform Access Token
tts_key = "xxxxxxxx" #IBM Watson Text To Speech Key
```

### set environment variablei on Google Cloud Platform
Download your service account key
https://cloud.google.com/docs/authentication/getting-started

```bash
export GOOGLE_APPLICATION_CREDENTIALS="[PATH]"
```

# Demo
```bash
$ python main.py 
```

```
=== Available Microphones: ===
# 0 - Built-in Microphone
# 1 - Earbud
========================================
1 / 2: Checking Microphones...
========================================
Select microphone [0]:
```
Press the ENTER KEY to start recording for 5 seconds
```
Please press the ENTER KEY to start recording!
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
recording for 5 sec...
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
finished recording
```
Output the detecting result and play the response.
```
1/1 [==============================] - 0s 84ms/step
========================================
Query text: I am so good.
Fulfillment text: Excellent. I'm here to help keep it that way.

Emotion Prediction: Happy
Context Prediction: Bedroom
========================================
Reply Emotion is 'GoodNews'
```
