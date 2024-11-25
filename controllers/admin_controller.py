from models import TextGenerationRequest

def validate_text_generation(request_id, is_validated):
    request = TextGenerationRequest.query.get(request_id)
    request.is_validated = is_validated
    db.session.commit()
