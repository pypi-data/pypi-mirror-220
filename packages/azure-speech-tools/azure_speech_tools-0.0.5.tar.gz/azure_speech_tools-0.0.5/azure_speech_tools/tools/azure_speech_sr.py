import os
import tempfile
import time
from promptflow import tool
from promptflow.connections import CustomConnection
from azure.cognitiveservices.speech import SpeechConfig, SpeechRecognizer, AudioConfig
from azure.storage.blob import BlobClient
import uuid

@tool
def azure_speech_sr(connection: CustomConnection, input_blob_url: str, language: str = 'en-US') -> str:
    
    temp_dir = tempfile.gettempdir()
    file_name = str(uuid.uuid4()) + ".wav"
    file_path = os.path.join(temp_dir, file_name)
    shared_access_key = connection.azure_storage_access_key
    credential = shared_access_key
    blob_client = BlobClient.from_blob_url(input_blob_url, credential=credential)
    with open(file=file_path, mode="wb") as audio_file:
        download_stream = blob_client.download_blob()
        audio_file.write(download_stream.readall())

    audio_config = AudioConfig(filename=file_path)
    speech_config = SpeechConfig(subscription=connection.api_key, region=connection.api_region)
    speech_config.speech_recognition_language = language
    speech_recognizer = SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    done = False
    def stop_cb(evt):
        speech_recognizer.stop_continuous_recognition()
        nonlocal done
        done = True
    
    all_results = []
    def handle_final_result(evt):
        all_results.append(evt.result.text)
    
    speech_recognizer.recognized.connect(handle_final_result)
    speech_recognizer.session_stopped.connect(stop_cb)
    speech_recognizer.canceled.connect(stop_cb)

    speech_recognizer.start_continuous_recognition()
    while not done:
        time.sleep(.5)
    return " ".join(all_results)
