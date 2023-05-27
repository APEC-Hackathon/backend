import os 

import fasttext
from transformers import M2M100ForConditionalGeneration, M2M100Tokenizer

translation_model = M2M100ForConditionalGeneration.from_pretrained("facebook/m2m100_418M")
tokenizer = M2M100Tokenizer.from_pretrained("facebook/m2m100_418M")
classification_model = fasttext.load_model(os.path.join(os.path.dirname(__file__), 'artifacts', 'lid.176.bin'))

def classify_language(text):
    prediction = classification_model.predict(text)
    label = prediction[0][0].replace('__label__', '')
    return label

def translate_text(text, source_lang, target_lang):
    tokenizer.src_lang = source_lang
    encoded_text = tokenizer(text, return_tensors='pt')
    generated_tokens = translation_model.generate(
        **encoded_text, 
        forced_bos_token_id=tokenizer.get_lang_id(target_lang), 
        max_length=256
    )
    decoded_tokens = tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)
    return decoded_tokens[0]

def translate(text, target_lang):
    try: 
        source_lang = classify_language(text)
        translation = translate_text(text, source_lang, target_lang)
        return translation
    except Exception as e:
        return text
    