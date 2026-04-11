from django.http import HttpResponse


def test_error(request):
    """Trigger a test error for Rollbar."""
    a = None
    a.hello()  # This will raise AttributeError
    return HttpResponse("This will not be reached")