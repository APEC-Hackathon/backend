from fastapi import APIRouter

from app.utils.translation import translate 


router = APIRouter()

@router.get('/')
def get_message_translated(text: str, target_lang: str) -> dict:
    """
    Translate a message to a target language
    """
    return {'translated': translate(text, target_lang)}
