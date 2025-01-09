import openai
import string


def get_relevant_words_from_gpt(context: str, transcription: str) -> set:
    """
    Extract words and phrases from a transcription that are directly related to the main subject 
    identified in the context.
    
    Args:
        context (str): Text containing the main subject/topic to focus on
        transcription (str): Text to extract relevant words/phrases from
        
    Returns:
        set: A set of words and phrases that are directly related to the context's main subject
    """
    

    prompt = f"""
    First, identify the main subject/topic from this context:
    {context}
    
    Then, from this transcription:
    {transcription}
    
    Extract ONLY words and phrases that are directly connected to context.
    Do not add any text that is not the words and phrases! if there are not words or phrases matched return empty string!!
    
    Rules:
    1. First determine the core subject/topic from the context
    2. Only return words/phrases that directly relate to that specific subject
    3. Exclude any words/phrases that are not directly related to the main subject
    4. Do not include common words, fillers, or general terms
    5. Return only the relevant words/phrases without any explanations or additional text
    6. Maintain meaningful phrases together when they relate to the subject
    
    Format your response as a simple list of words and phrases, one per line.
    """

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": """
                You are a precise extractor of subject-relevant terms.
                Your sole task is to:
                1. Identify the main subject from the context
                2. Extract only words and phrases from the transcription that directly relate to that subject
                3. Return them as a simple list, one item per line
                4. if there is no words or phrases relavent return an empty string
                Do not include any explanations or additional text.
                """
            },
            {"role": "user", "content": prompt}
        ],
        max_tokens=150,
        temperature=0
    )
    
    # Get the response and split into lines
    relevant_terms = response['choices'][0]['message']['content'].strip().split('\n')
    
    # Clean each term while preserving meaningful phrases
    cleaned_terms = {
        term.strip().lower().translate(str.maketrans('', '', string.punctuation))
        for term in relevant_terms
        if term.strip()
    }
    
    return cleaned_terms
    