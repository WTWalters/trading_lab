# dashboard/views.py (continued)

def educational_guidance_view(request):
    """
    View function for providing educational context about trading concepts.
    Retrieves educational guidance from the Gemini API for a specific topic.
    
    Expected request parameters:
    - topic (str): The trading topic to get an explanation for
                  (e.g., 'volume_confirmation', 'atr_stop')
    
    Returns JSON response with explanation text for AJAX requests,
    or renders a simple template for direct URL access.
    """
    topic = request.GET.get('topic', 'default')
    
    # Call the educational guidance module
    explanation = get_educational_context(topic)
    
    # Return JSON for AJAX requests
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'explanation': explanation,
            'topic': topic
        })
    
    # For direct URL access, render a template
    context = {
        'explanation': explanation,
        'topic': topic
    }
    return render(request, 'dashboard/educational_guidance.html', context)
