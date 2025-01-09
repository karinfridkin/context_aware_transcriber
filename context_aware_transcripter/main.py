from context_extraction import extract_text_from_file, extract_text_from_url
from gpt_utils import get_relevant_words_from_gpt
from transcipter import transcribe_chunk, is_silent
from display import display_transcription_with_highlights
from record import record_chunk

import pyaudio
import os
import time
from tkinter import Tk, Button, filedialog, simpledialog

def main():
    # Create the Tkinter window for GUI
    root = Tk()
    root.title("Select Context Source")
    root.geometry("300x200")

    # Hide the root window initially
    root.withdraw()

    # Define context variable and context_exist
    context_exist = False
    context = None

    # Function to handle file upload
    def upload_file():
        nonlocal context_exist, context
        file_path = filedialog.askopenfilename(title="Select a context file", filetypes=[("Text Files", "*.txt")])
        if file_path:
            context = extract_text_from_file(file_path)
            print("Context loaded from file.")
            context_exist = True
            root.quit()
            root.destroy()
        else:
            print("No file selected. Exiting.")
            root.quit()
            root.destroy()

    # Function to handle URL input
    def provide_url():
        nonlocal context_exist, context
        url = simpledialog.askstring("Input", "Enter the URL for context:")
        if url:
            context = extract_text_from_url(url)
            print("Context loaded from URL.")
            context_exist = True
            root.quit()
            root.destroy()
        else:
            print("No URL provided. Exiting.")
            root.quit()
            root.destroy()

    # Buttons for file upload and URL input
    file_button = Button(root, text="Upload Context File", command=upload_file)
    file_button.pack(pady=20)

    url_button = Button(root, text="Provide Context URL", command=provide_url)
    url_button.pack(pady=20)

    # Run the Tkinter event loop to display the window
    root.deiconify()
    root.mainloop()

    # Now proceed with the next steps using the 'context' variable
    if context_exist:
        # Initialize PyAudio stream and other variables
        p = pyaudio.PyAudio()
        stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=1024)

        accumulated_transcription = ""

        try:
            while True:
                # chunk_file = "harvard.wav" example sound file for texting.
                chunk_file = "temp_chunk.wav"
                record_chunk(p, stream, chunk_file)

                # Ignore silence
                if is_silent(chunk_file):
                    continue

                # Transcribe the chunk
                transcription = transcribe_chunk(chunk_file)

                # Get relevant words from GPT based on the context
                matched_keywords = get_relevant_words_from_gpt(context, transcription)

                # Append the new transcription to the accumulated transcription
                accumulated_transcription += transcription + " "

                # Display the transcription with highlighted keywords
                display_transcription_with_highlights(transcription, matched_keywords)

                # Clean up the chunk file after processing
                os.remove(chunk_file)

                # Small delay to avoid overwhelming the terminal with too many updates
                time.sleep(0.1)

        except KeyboardInterrupt:
            print("Stopping...")

            # Write the accumulated transcription to the log file
            with open("log.txt", "w") as log_file:
                log_file.write(accumulated_transcription)

        finally:
            print("\nLOG:", accumulated_transcription)
            stream.stop_stream()
            stream.close()
            p.terminate()

if __name__ == "__main__":
    main()
