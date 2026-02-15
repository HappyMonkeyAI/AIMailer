from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Subscriber

def unsubscribe(request, token):
    subscriber = get_object_or_404(Subscriber, unsubscribe_token=token)

    if subscriber.status != 'unsubscribed':
        subscriber.status = 'unsubscribed'
        subscriber.unsubscribed_at = timezone.now()
        subscriber.save()

    return render(request, 'newsletters/unsubscribe_success.html')
