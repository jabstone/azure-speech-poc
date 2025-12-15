import azure.cognitiveservices.speech as speechsdk

# Replace with your Azure Speech credentials
speech_key = "THIS IS WHERE YOUR SPEECH KEY GOES FROM AZURE"
service_region = "eastus"  # e.g. "eastus"

# Configure the speech synthesizer
speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
speech_config.speech_synthesis_voice_name = "el-GR-NestorasNeural"

ph = "k a l e ˈm ɛ ɾ a"  # IPA pronunciation for "Καλημέρα" (Good morning in Greek)
# SSML with IPA pronunciation
ssml_string = f"""
<speak version='1.0' xml:lang='el-GR'>
  <voice name='el-GR-NestorasNeural'>
    <prosody rate="medium" pitch="0%">
      <phoneme alphabet='ipa' ph='{ph}'>Καλημέρα</phoneme>
    </prosody>
  </voice>
</speak>

"""

# Configure audio output to file
audio_filename = "output.wav"
audio_config = speechsdk.audio.AudioOutputConfig(filename=audio_filename)

# Create synthesizer with file output
synthesizer = speechsdk.SpeechSynthesizer(
    speech_config=speech_config, audio_config=audio_config
)

# Speak SSML with IPA and save to file
result = synthesizer.speak_ssml_async(ssml_string).get()

# Check result
if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
    print(f"✅ Speech synthesized and saved to {audio_filename}")

    # Convert WAV to MP3 (requires pydub and ffmpeg)
    try:
        from pydub import AudioSegment

        # Load WAV file and convert to MP3
        audio = AudioSegment.from_wav(audio_filename)
        mp3_filename = "output.mp3"
        audio.export(mp3_filename, format="mp3")

        print(f"✅ Audio converted and saved as {mp3_filename}")

        # Optional: Remove the temporary WAV file
        import os

        os.remove(audio_filename)
        print(f"🗑️ Temporary file {audio_filename} removed")

    except ImportError:
        print("⚠️ pydub not installed. Audio saved as WAV format.")
        print("To convert to MP3, install pydub: pip install pydub")
        print("You'll also need ffmpeg installed on your system.")

elif result.reason == speechsdk.ResultReason.Canceled:
    cancellation = result.cancellation_details
    print("❌ Canceled: {}".format(cancellation.reason))
    if cancellation.reason == speechsdk.CancellationReason.Error:
        print("Error details: {}".format(cancellation.error_details))
