from flask import Flask, render_template, request
import requests
import json
import re
from transformers import pipeline
from youtube_transcript_api import YouTubeTranscriptApi

app = Flask(__name__)
summarizer = pipeline("summarization", model="t5-base", tokenizer="t5-base", framework="tf")
@app.route('/',methods=['GET'])
def home():
    return render_template('index.html',content="")

@app.route('/summarize', methods=['POST'])
def summarize_transcript():
    if request.method == "POST":
        video_url = request.form.get('video-url')
        video_id=video_url.split("=")[1]

        print(video_url)

        YouTubeTranscriptApi.get_transcript(video_id)
        transcript=YouTubeTranscriptApi.get_transcript(video_id)

        result = ""
        for i in transcript:
            result += ' ' + i['text']
        print(len(result))

        num_iters = int(len(result)/1000)
        summarized_text = []
        for i in range(0, num_iters + 1):
            start = 0
            start = i * 1000
            end = (i + 1) * 1000
            #print("input text \n" + result[start:end])
            out = summarizer(result[start:end])
            out = out[0]
            out = out['summary_text']
            print("Summarized text\n"+out)
            summarized_text.append(out)
        return render_template("index.html",content=" ".join(summarized_text))

if __name__ == '__main__':
    app.run(debug=True)