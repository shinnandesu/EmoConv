# EmoConv
- Dialogflow API
- IBM Watson Text to Speech API 

# System Requirements
The deep learning system is written in `python3`, specifically `tensorflow` and `keras`.


```bash
$ git clone https://github.com/shinnandesu/EmoConv.git
$ pip install tensorflow==1.12.0 keras==2.2.4 wget
```
Install the Watson Developer SDK and Dialogflow SDK

```bash
$ pip install --upgrade watson-developer-cloud
$ pip install dialogflow
```

# Setting
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

