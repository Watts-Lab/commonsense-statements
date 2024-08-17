import openai
import os
import re
import pandas as pd

# set up OpenAI credentials
openai.api_key = os.environ.get('OPENAI_API_KEY')

# define supported languages
languages = {
    'ar': 'Arabic',
    'bn': 'Bengali',
    'en': 'English',
    'es': 'Spanish',
    'fr': 'French',
    'hi': 'Hindi',
    'ja': 'Japanese',
    'pt': 'Portuguese',
    'ru': 'Russian',
    'zh': 'Chinese'
}

# function that sets up API
def chat_completion_function(lng, user_prompt):
    system_prompt = f"""
                    You are a language processing assistant. Given this statement in {languages[lng]}, perform the following steps:
                    1. Capitalize the first letter (if applicable for the language).
                    2. Remove leading and trailing punctuation.
                    3. Ensure the sentence ends with the appropriate full-stop punctuation native to the language (e.g., । for Bengali and Hindi, 。 for Japanese and Chinese).
                    4. Do not change the capitalization of any other words within the sentence besides the first word, including proper nouns, event names, and common words—preserve all original capitalization as given by the user.
                    5. Do not introduce any changes to the vocabulary, meaning, or phrasing. Preserve the exact words provided.
                    6. Do not introduce any additional punctuation, symbols, or special characters.

                    Return only the cleaned statement in the same format given by the user, without any additional text, explanations, or changes to the proper nouns' capitalization or vocabulary. Here are some examples in 10 different languages:
                    - '"Social Security and Medicare are programs that politicians can protect'" should be '"Social Security and Medicare are programs that politicians can protect."'
                    - "el Seguro Social y Medicare son programas que los políticos pueden proteger" should be "El seguro social y medicare son programas que los políticos pueden proteger."
                    - "সামাজিক নিরাপত্তা এবং মেডিকেয়ার হল এমন প্রোগ্রাম যা রাজনীতিবিদরা রক্ষা করতে পারেন" should be "সামাজিক নিরাপত্তা এবং মেডিকেয়ার হল এমন প্রোগ্রাম যা রাজনীতিবিদরা রক্ষা করতে পারেন।"
                    - "社会保障和医疗保险是政治家可以保护的计划" should be "社会保障和医疗保险是政客可以保护的计划。"
                    - "إن الضمان الاجتماعي والرعاية الطبية من البرامج التي يمكن للسياسيين حمايتها" should be "إن الضمان الاجتماعي والرعاية الطبية من البرامج التي يمكن للسياسيين حمايتها."
                    - "la sécurité sociale et Medicare sont des programmes que les politiciens peuvent protéger" should be "La sécurité sociale et Medicare sont des programmes que les politiciens peuvent protéger."
                    - "सामाजिक सुरक्षा और मेडिकेयर ऐसे कार्यक्रम हैं जिनकी रक्षा राजनेता कर सकते हैं" should be "सामाजिक सुरक्षा और मेडिकेयर ऐसे कार्यक्रम हैं जिनकी रक्षा राजनेता कर सकते हैं।"
                    - "社会保障とメディケアは政治家が守ることができる制度である" should be "社会保障とメディケアは政治家が守ることができるプログラムです。"
                    - "Социальное обеспечение и Medicare — это программы, которые политики могут защитить" should be "Социальное обеспечение и Medicare — это программы, которые политики могут защитить."
                    - "a Segurança Social e o Medicare são programas que os políticos podem proteger" should be "A Segurança Social e o Medicare são programas que os políticos podem proteger."
                    """
    try:
        completion = openai.chat.completions.create(
            model='gpt-3.5-turbo',
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
        )

        response_content = completion.choices[0].message.content
        return response_content.strip()
    except Exception as e:
        print(f"Error: {e}")
        return None

# process files in raw_statements directory 
def process_files(directory):
    files_cleaned = set()
    count = 0

    # check if all files have already been cleaned
    for filename in os.listdir(directory):
        if filename.endswith('.csv'):
            count += 1 
            if (filename.split('.')[0].split('_')[-1] == 'cleaned'):
                files_cleaned.add(filename)
    
    if count == len(files_cleaned):
        print("All files have already been cleaned.")
        return
    
    for filename in os.listdir(directory):
        if filename.endswith('.csv') and filename not in files_cleaned:
            # extract the language code from the file
            lng_group = re.search(r'_([a-z]{2})(?:_cleaned)?\.csv$', filename) 

            if lng_group:
                lng = lng_group.group(1)
                print(f"Detected language: {languages[lng]}")
            else:
                print(f"Error: Unable to determine language for {filename}")
                continue

            filepath = os.path.join(directory, filename)
            df = pd.read_csv(filepath)
            cleaned_statements = []
            
            print(f"Processing {filename}...")

            # clean each statement in the file
            for statement in df['statement']:
                cleaned_statement = chat_completion_function(lng, statement)
                print(cleaned_statement)
                cleaned_statements.append(cleaned_statement)
 
            df['statement'] = cleaned_statements

            # save cleaned data back to the file
            df.to_csv(filepath, index=False)
            cleaned_filename = f"{os.path.splitext(filename)[0]}_cleaned.csv"
            cleaned_filepath = os.path.join(directory, cleaned_filename)
            os.rename(filepath, cleaned_filepath)
            print(f"Cleaned data saved back to {filepath} and renamed file to {cleaned_filepath}")
        

if __name__ == '__main__':
    process_files('raw_statements')