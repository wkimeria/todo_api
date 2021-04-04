import json
def ensure_json(request):
    
    # Data must be JSON
    try:  
        data = request.get_json()
        return data
    
    except Exception as e: 
        return None
        