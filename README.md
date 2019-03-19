# EmoConv



# System Requirements
The deep learning system is written in `python3`, specifically `tensorflow` and `keras`.


```bash
$ git clone https://github.com/FIGLAB/ubicoustics.git
$ pip install tensorflow==1.12.0 keras==2.2.4 wget
```

# Setting

```bash
$ touch config.py
```
```python
g_project_id = 'xxxxxxxx' #Google Cloud Platform project ID 
g_client_access_token = 'xxxxxxxx' #Google Cloud Platform Access Token
tts_key = "xxxxxxxx" #IBM Watson Text To Speech Key
```


# Example Demos
```bash
$ python main.py 
```