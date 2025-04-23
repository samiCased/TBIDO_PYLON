from django.conf import settings
from django.core.cache import cache
from.models import *
from .forms import *
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.urls import reverse
import random
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.utils.timezone import now

from datetime import datetime

def logo(request):
    # Cache the logo to avoid hitting the database on every request
    logo_id = getattr(request, 'logo_id', None)
    if logo_id is None:
        logo_id = cache.get('logo_id')
        if logo_id is None:
            logo = Logo.objects.get(id=1)  # Assuming there's only one logo
            cache.set('logo_id', logo.id, timeout=60 * 60)  # Cache for 1 hour
            logo_id = logo.id
    return {'logo': Logo.objects.get(id=logo_id)}

def profile(request):
    user = request.user

    if hasattr(user, 'officer'):
        profile = user.officer
    elif hasattr(user, 'member'):
        profile = user.member
    elif hasattr(user, 'guest'):
        profile = user.guest
    else:
        profile = None

    return {'profile': profile}