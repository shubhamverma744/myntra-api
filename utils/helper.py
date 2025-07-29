import uuid

def generate_unique_filename(filename):
    ext = filename.split('.')[-1]
    return f"{uuid.uuid4().hex}.{ext}"
