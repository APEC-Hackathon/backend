import random

DEFAULT_AVA_URL = 'https://vgxwzvhdgqdrcezoxblv.supabase.co/storage/v1/object/public/avatars/default-ava.png'

DEFAULT_PROBLEM_IMG_URLS = [
    'https://vgxwzvhdgqdrcezoxblv.supabase.co/storage/v1/object/public/posts/problems/prob-1.png',
    'https://vgxwzvhdgqdrcezoxblv.supabase.co/storage/v1/object/public/posts/problems/prob-2.png',
    'https://vgxwzvhdgqdrcezoxblv.supabase.co/storage/v1/object/public/posts/problems/prob-3.png',
    'https://vgxwzvhdgqdrcezoxblv.supabase.co/storage/v1/object/public/posts/problems/prob-4.png',
]

DEFAULT_COLLABORATION_IMG_URLS = [
    'https://vgxwzvhdgqdrcezoxblv.supabase.co/storage/v1/object/public/posts/collaborations/collab-1.png'
    'https://vgxwzvhdgqdrcezoxblv.supabase.co/storage/v1/object/public/posts/collaborations/collab-2.png'
    'https://vgxwzvhdgqdrcezoxblv.supabase.co/storage/v1/object/public/posts/collaborations/collab-3.png'
    'https://vgxwzvhdgqdrcezoxblv.supabase.co/storage/v1/object/public/posts/collaborations/collab-4.png'
]

def get_default_ava_url():
    return DEFAULT_AVA_URL

def get_default_problem_img_url():
    return random.choice(DEFAULT_PROBLEM_IMG_URLS)

def get_default_collaboration_img_url():
    return random.choice(DEFAULT_COLLABORATION_IMG_URLS)
