from colorama import init, Fore
import re

# Initialize colorama for compatibility on all platforms
init(autoreset=True)

# Function to colorize and display relevant words in real-time
def display_transcription_with_highlights(transcription: str, matched_keywords: set):
    # Iterate over the matched keywords
    highlighted_transcription = transcription
    
    # Loop through the keywords and replace them with highlighted versions
    for keyword in matched_keywords:
        # Create a case-insensitive regex pattern to match the keyword
        pattern = r'(?i)\b' + re.escape(keyword) + r'\b'
        # Replace the matched keyword with highlighted keyword (preserve case)
        highlighted_transcription = re.sub(pattern, lambda m: Fore.GREEN + m.group(0) + Fore.RESET, highlighted_transcription)
    
    # Print the highlighted transcription
    print(highlighted_transcription)
