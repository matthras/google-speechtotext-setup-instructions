# How to Setup Your System to use Google Cloud's Speech-To-Text to Transcribe Podcasts (or any audio file)

The purpose of this repo is for me to store scripts and instructions on how to transcribe podcasts using [Google Cloud's Speech-to-Text](https://cloud.google.com/speech-to-text/), although I'm aiming to write this in a more general manner so that anyone stumbling across this should be able to replicate my process. This is not meant to be perfect, merely what I've figured out. Naturally, the usual disclaimer applies in that all of this is correct at the time of writing, and that there may be changes to Google's services in future.

Once everything is setup correctly, you should be able to follow an opinionated step-by-step process to obtain a transcription (text file) of any audio file by running a Python script (of which a general version is provided in this repo).

## Assumptions

* I'm currently using Windows 10 so the instructions are tailored towards that. 
* You should at least be an amateur programmer who is familiar with using the command line and knows how to run a script.
* Your internet connection should have sufficiently fast upload (at least 1MB/s) since you'll be uploading large audio files to Google Cloud as part of the process.
* You have a Google account, since you're going to be using Google-related services. For most this shouldn't be a problem, but I do want to acknowledge those who avoid Google products for privacy reasons.

**Nice-To-Haves**

* Basic knowledge in audio files.

## Setup

### Setting up a Cloud Console Project and Installing the Google Cloud SDK

As a litmus test and sanity check, I recommend following the [gcloud Quickstart](https://cloud.google.com/speech-to-text/docs/quickstart-gcloud) as the steps listed there are also part of the initial setup.

1. [gcloud Quickstart] Set up a Cloud Console Project - follow the instructions as given in the link.

    * I ended up putting my JSON file (containing the private key) in the same folder as my podcast transcript folder since I'm not using gcloud for anything else. Please take note of the generated email address used in that file, you'll need it for later.

2. [gcloud QuickStart] Set the environment variable - the instructions in the link only enable you to do this for your current cmd/powershell/terminal, but you'll want to save this option more permanently on your computer so that you don't have to set it everytime you want to run a transcription.

    * In Windows 10, you can open the Start Menu and type in 'environment variables' ("Edit the system environment variables"), then click on 'Environment Variables...' in the box that pops up. 

3. [gcloud QuickStart] Install the Google Cloud SDK - follow the link in the given link (which should result in [this one](https://cloud.google.com/sdk/docs/)) and follow the instructions given.

    * After this you can try the 'Make an audio transcription request' in the gcloud Quickstart link. 

4. Install the client library for whichever language you're going to use. [Instructions here (including Python).](https://cloud.google.com/speech-to-text/docs/reference/libraries)

### Setting up a Google Cloud Bucket for storing your audio files

Note: I tried doing the process using the terminal commands and FLAC files on my computer, but consistently got a server message that file size was too large. Using a Google Cloud Bucket sidesteps this problem.

1. Go to `cloud.google.com`

2. In the left menu, go to Storage > Storage > Browser, and create a bucket. All the default options should be fine.

3. Once your bucket is created, you should be able to click on it once via the Browser, which will open a menu on the right. Click on 'Add Member'

4. Copy/paste the email address given in your JSON file as a New Member and give it a 'Storage Admin' role, and click 'Save'.

## Step-By-Step Process

1. Assuming you have your audio file and `gcloud-script.py` in the same folder, open a command prompt and convert the audio file to FLAC using `ffmpeg`: `ffmpeg -i audiofile.mp3 -ac 1 audiofile.flac`

    * `audiofile.mp3` should be replaced with the name of the file you want to convert (if that wasn't immediately obvious!).
    * `-ac 1` ensures the output FLAC file has only one audio channel (ac). Some podcasts can have more than one audio channel (e.g. due to separate microphones for each speaker), but what happens in Google's Speech-To-Text is that all channels get transcribed separately, which results in the output file having repeated sections. 
    * FLAC is a lossless (i.e. no/minimal compression) audio file, meaning that the resulting filesize will be much larger.

2. Upload the FLAC file to your Google Cloud Bucket.

    * For slower connections this can take a while so please be cognizant of this and be aware that this may put a halt to your other internet activities.

3. Obtain the URI to the file you just uploaded. It should look something like `gs://[BUCKET NAME]/[FILE NAME.flac]`. Copy this link to the Python script to the URI link as indicated. Edit any other variables as needed.

4. Run the Python script and wait - as a rough rule of thumb, the transcription process on Google Cloud should take at most the length of the audio itself. The resulting file will appear in the same folder as this script 'transcript.txt' (or whatever filename you've changed it to).