import openai
import wave
import numpy as np

def transcribe_chunk(file_path):
    with open(file_path, "rb") as audio_file:
        response = openai.Audio.transcribe(
            "whisper-1",
            audio_file,
            language="en",
            temperature=0,          
            prompt="Transcribe the following speech clearly and accurately.",
            response_format="text",  
        )
    return response

def is_silent(file_path, threshold=0.05, min_duration=1):
<<<<<<< HEAD
    with wave.open(file_path, 'rb') as wf:
        # Read audio data
        frames = wf.readframes(wf.getnframes())
        audio_data = np.frombuffer(frames, dtype=np.int16)
        
        # Convert to float32 for easier calculations
        audio_float = audio_data.astype(np.float32) / 32767.0
        
        # Calculate RMS value for volume
        frame_length = int(wf.getframerate() * min_duration)
        frames = [audio_float[i:i + frame_length] for i in range(0, len(audio_float), frame_length)]
        
        # Check if any frame is above threshold
        for frame in frames:
            rms = np.sqrt(np.mean(np.square(frame)))
            if rms > threshold:
                return False
                
        return True
        
=======
    try:
        with wave.open(file_path, 'rb') as wf:
            # Read audio data
            frames = wf.readframes(wf.getnframes())
            audio_data = np.frombuffer(frames, dtype=np.int16)
            
            # Convert to float32 for easier calculations
            audio_float = audio_data.astype(np.float32) / 32767.0
            
            # Calculate RMS value for volume
            frame_length = int(wf.getframerate() * min_duration)
            frames = [audio_float[i:i + frame_length] for i in range(0, len(audio_float), frame_length)]
            
            # Check if any frame is above threshold
            for frame in frames:
                rms = np.sqrt(np.mean(np.square(frame)))
                if rms > threshold:
                    return False
                    
            return True
            
    except Exception as e:
        print(f"Error checking silence: {e}")
        return True
>>>>>>> 8077355 (the transcription works well. the record is working - but the sound is not perfect)
