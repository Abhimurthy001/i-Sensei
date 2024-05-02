import boto3
import streamlit as st
from contextlib import closing
import os
import sys
import subprocess
from tempfile import gettempdir
from dotenv import load_dotenv

load_dotenv()

def synthesize_speech(text):
    aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
    aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")

    session = boto3.Session(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name="us-east-1"
    )

    polly = session.client("polly")
    response = polly.synthesize_speech(
        Text=text,
        OutputFormat="mp3",
        VoiceId="Joanna"
    )
    if "AudioStream" in response:
        with closing(response["AudioStream"]) as stream:
            output = os.path.join(gettempdir(), "temp_audio.mp3")

            try:
                with open(output, "wb") as file:
                    file.write(stream.read())
            except IOError as error:
                print(error)
                sys.exit(-1)
    else:
        print("Could not stream audio")
        sys.exit(-1)
    return output
