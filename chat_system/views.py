from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import redirect, render

from .forms import MessageForm
from .models import Message


@login_required
def inbox(request):
    messages_qs = Message.objects.filter(Q(recipient=request.user) | Q(sender=request.user)).select_related('sender', 'recipient')
    return render(request, 'chat_system/inbox.html', {'conversation': messages_qs})


@login_required
def compose(request):
    User = get_user_model()
    if request.user.is_customer:
        recipients = User.objects.filter(role=User.SHOPKEEPER, shopkeeper_profile__is_active=True)
    elif request.user.is_shopkeeper:
        recipients = User.objects.filter(role=User.CUSTOMER)
    else:
        recipients = User.objects.exclude(pk=request.user.pk)
    form = MessageForm(request.POST or None, recipients=recipients)
    if request.method == 'POST' and form.is_valid():
        message = form.save(commit=False)
        message.sender = request.user
        message.save()
        messages.success(request, 'Message sent.')
        return redirect('chat_system:inbox')
    return render(request, 'chat_system/compose.html', {'form': form})

# Create your views here.
