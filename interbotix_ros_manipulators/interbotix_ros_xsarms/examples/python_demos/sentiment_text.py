from torch import negative
from transformers import AutoModelForSequenceClassification
from transformers import TFAutoModelForSequenceClassification
from transformers import AutoTokenizer
import numpy as np
from scipy.special import softmax
import csv
import urllib.request
import end_existence

import sounddevice as sd
from scipy.io.wavfile import write
import wavio as wv
import whisper
from interbotix_xs_modules.arm import InterbotixManipulatorXS

whisper_model = whisper.load_model("base")

def whisper_transcribe(filename):
    

    # load audio and pad/trim it to fit 30 seconds
    audio = whisper.load_audio(filename)
    audio = whisper.pad_or_trim(audio)

    # make log-Mel spectrogram and move to the same device as the model
    mel = whisper.log_mel_spectrogram(audio).to(whisper_model.device)

    # detect the spoken language
    _, probs = whisper_model.detect_language(mel)
    print(f"Detected language: {max(probs, key=probs.get)}")

    # decode the audio
    translate_options = whisper.DecodingOptions(task='translate')
    translate_result = whisper.decode(whisper_model, mel, translate_options)

    transribe_options = whisper.DecodingOptions()
    transcribe_result = whisper.decode(whisper_model, mel, transribe_options)

    # print the recognized text

    return (translate_result.text, transcribe_result.text)

# Sampling frequency
freq = 44100

# Recording duration
duration = 5

# Preprocess text (username and link placeholders)
def preprocess(text):
    return text

# Tasks:
# emoji, emotion, hate, irony, offensive, sentiment
# stance/abortion, stance/atheism, stance/climate, stance/feminist, stance/hillary

task='sentiment'
MODEL =  f"cardiffnlp/twitter-roberta-base-{task}"
tokenizer = AutoTokenizer.from_pretrained(MODEL)

# download label mapping
labels=[]
mapping_link = f"https://raw.githubusercontent.com/cardiffnlp/tweeteval/main/datasets/{task}/mapping.txt"
with urllib.request.urlopen(mapping_link) as f:
    html = f.read().decode('utf-8').split("\n")
    csvreader = csv.reader(html, delimiter='\t')
labels = [row[1] for row in csvreader if len(row) > 1]

# PT
model = AutoModelForSequenceClassification.from_pretrained(MODEL)
#odel.save_pretrained(MODEL)



def rank(text):
    text = preprocess(text)
    encoded_input = tokenizer(text, return_tensors='pt')
    output = model(**encoded_input)
    scores = output[0][0].detach().numpy()
    scores = softmax(scores)

    ranking = np.argsort(scores)
    ranking = ranking[::-1]
    sentiment_result = {}
    for i in range(scores.shape[0]):
        l = labels[ranking[i]]
        s = scores[ranking[i]]
        sentiment_result[l] = s
        print(f"{i+1}) {l} {np.round(float(s), 4)}")
    return sentiment_result

def clamp(num, min_value, max_value):
   return max(min(num, max_value), min_value)

my_sentiment = { 'positive': 0.33, 'negative': 0.33, 'neutral': 0.33}
bot = InterbotixManipulatorXS("px150", "arm", "gripper")



while True:
    print('type anything to start recording (5 seconds)')
    text = input()
    if text == 'quit':
        break
    elif text == 'reset':
        bot.arm.go_to_home_pose()
        continue



    # Start recorder with the given values of 
    # duration and sample frequency
    recording = sd.rec(int(duration * freq), samplerate=freq, channels=2)

    # Record audio for the given number of seconds
    print('Recording start')
    sd.wait()
    print('Recording end')
    filename = 'temp.wav'
    write(filename, freq, recording)
    translated, raw = whisper_transcribe(filename)
    print(f'I heard: "{raw}"')
    print(f'I translated it as: "{translated}"')
    res = rank(translated)

    my_sentiment['positive'] = (my_sentiment['positive'] + res['positive'])/ 2
    my_sentiment['negative'] = (my_sentiment['negative'] + res['negative'])/ 2
    my_sentiment['neutral'] = (my_sentiment['neutral'] + res['neutral'])/ 2

    print(my_sentiment)
    if my_sentiment['positive'] > 0.8:
        # do happy dance
        print('I am so happy im going to do my happy little robot dance')
        
        bot.arm.set_single_joint_position("waist", np.pi/2.0)
        bot.arm.set_single_joint_position("waist", -np.pi/2.0)
        bot.arm.set_single_joint_position("waist", np.pi/2.0)
        bot.arm.set_single_joint_position("waist", -np.pi/2.0)
        bot.arm.set_single_joint_position("waist", np.pi/2.0)
        bot.arm.set_single_joint_position("waist", -np.pi/2.0)
        bot.arm.set_single_joint_position("waist", 0)
    elif my_sentiment['negative'] > 0.8:
        print('goodbye cruel world....')
        end_existence.main()
        break
    else:
        d_pos = res['positive'] - my_sentiment['positive']
        d_neg = res['negative'] - my_sentiment['negative'] 
        d_total = d_pos - d_neg
        v = clamp(d_total, -0.05, 0.05)
        bot.arm.set_ee_cartesian_trajectory(x=v, z=v)
    



bot.arm.go_to_sleep_pose()

    

"""
while(True):
    text = input()


"""