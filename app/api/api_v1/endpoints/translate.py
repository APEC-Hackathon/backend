from fastapi import APIRouter

from app.utils.translation import translate 


router = APIRouter()

@router.get('/')
def get_message_translated(text: str, target_lang: str):
    """
    Translate a message to a target language
    """
    return translate(text, target_lang)
