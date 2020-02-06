from google.cloud import speech_v1
from google.cloud.speech_v1 import enums

## Adapted from: https://cloud.google.com/speech-to-text/docs/async-recognize

def sample_long_running_recognize():
    """
    Transcribe long audio file from Cloud Storage using asynchronous speech
    recognition
    """
    #############################################
    # Initialise variables - EDIT THESE VARIABLES
    #############################################

    # This is where the link to the audio file in your Google Cloud Bucket goes
    storage_uri = 'gs://[BUCKET NAME]/[FILENAME].flac'

    # Sample rate in Hertz of the audio data sent - leave this as default, unless you 
    sample_rate_hertz = 44100

    # The language of the supplied audio. Google Cloud is capable of auto-detecting, but specifying will save effort.
    language_code = "en-US"

    # Number of channels - this assumes you've mixed the file down into a single audio channel via ffmpeg as per the given instructions.
    audio_channel_count = 1

    #############################################

    client = speech_v1.SpeechClient()
    # Encoding of audio data sent. This sample sets this explicitly.
    # This field is optional for FLAC and WAV audio formats.
    encoding = enums.RecognitionConfig.AudioEncoding.FLAC
    config = {
        "language_code": language_code,
        "audio_channel_count": audio_channel_count,
    }
    audio = {"uri": storage_uri}

    operation = client.long_running_recognize(config, audio)

    print(u"Waiting for operation to complete...")
    response = operation.result()
    transcriptfile = open("transcript.txt","w")
    for result in response.results:
        # First alternative is the most probable result
        alternative = result.alternatives[0]
        transcriptfile.write(u"{}\n".format(alternative.transcript))
    transcriptfile.close()
    print(u"Transcription done!")

sample_long_running_recognize()