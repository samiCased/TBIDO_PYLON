from datetime import datetime
import json
import random
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.offline import plot

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.utils.timezone import now
from django.views.decorators.http import require_http_methods
from django.views.generic import TemplateView
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.utils.html import escape
from dateutil import parser as date_parser
from django.db.models import Q
from collections import defaultdict, namedtuple

from django.http import HttpResponseBadRequest


# from datetime import isoformat

from .forms import *
from .models import *

@login_required
def mark_as_favorite(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user.is_authenticated:
        Favorite.objects.create(user=request.user, post=post)
        return HttpResponseRedirect(reverse('favorite_posts'))
    else:
        return redirect('login')

@login_required
def favorite_posts(request):
    if request.user.is_authenticated:
        favorites = Favorite.objects.filter(user=request.user).order_by('-created_at')
        return render(request, 'favorite_posts.html', {'favorites': favorites})
    else:
        return redirect('login')
    
def videos_page(request):
    videoposts = VideoPost.objects.order_by('-Date')

    context = {
        'videoposts': videoposts,
    }

    return render(request, 'videos.html', context)


def sponsor_page(request):
    sponsorposts = SponsorPost.objects.order_by('-Date')

    context = {
        'sponsorposts': sponsorposts,
    }

    return render(request, 'sponsors.html', context)

def candidates_page(request):
    candidates = Candidate.objects.all()
    return render(request, 'candidates.html', {'candidates': candidates})

@login_required
def candidates_register(request):
    if request.method == 'POST':
        form = CandidateForm(request.POST, request.FILES)
        if form.is_valid():
            candidate = form.save(commit=False)
            candidate.save()
            return redirect('candidates_page')
    else:
        form = CandidateForm()

    return render(request, 'candidate_register.html', {'form': form})

def landing_page(request):
    logo = Logo.objects.get(id=1)
    all_posts = Post.objects.all()
    misc = Misc.objects.all()
    misc1 = Misc.objects.filter(id=1)
    random_post = random.choice(all_posts) if all_posts else None
    other_posts = Post.objects.exclude(id=random_post.id) if random_post else []
    
    current_season = Season.objects.filter(start_year__lte=timezone.now().year, end_year__gte=timezone.now().year).first()
    if current_season:
        future_schedules = MentoringSchedule.objects.filter(seasongrouping__season=current_season, session_time__gte=timezone.now()).order_by('session_time')
        most_recent_schedule = future_schedules.first()
        schedules = MentoringSchedule.objects.filter(seasongrouping__season=current_season).order_by('session_time')
        mentoring_sessions = MentoringSession.objects.filter(seasongrouping__season=current_season).order_by('-date')[:5]
    else:
        schedules = MentoringSchedule.objects.none()
        # event_schedules = EventSchedule.objects.none()
        most_recent_schedule = None
        mentoring_sessions = MentoringSession.objects.none()

    partner_logos = PartnerLogo.objects.all()

    context = {
        'random_post': random_post,
        'other_posts': other_posts,
        'schedules': schedules,
        # 'event_schedules': event_schedules,
        'current_season': current_season,
        'mentoring_sessions': mentoring_sessions, 
        'most_recent_schedule': most_recent_schedule,
        'most_recent_schedule_date': most_recent_schedule.session_time.strftime('%Y-%m-%d %H:%M:%S') if most_recent_schedule else '',
        'logo': logo,
        'misc': misc,
        'misc1': misc1,
        'partner_logos': partner_logos,
    }

    return render(request, 'landing_page.html', context)

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            user_type = form.cleaned_data.get('user_type')
            if user_type == 'officer':
                return redirect('create_officer')
            elif user_type == 'member':
                return redirect('create_member')
            elif user_type == 'guest':
                return redirect('create_guest')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            officer = Officer.objects.filter(user=user).first()
            member = Member.objects.filter(user=user).first()
            guest = Guest.objects.filter(user=user).first()

            if not officer and not member and not guest:
                return redirect('register')
            else:
                return HttpResponseRedirect(reverse('home'))
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password.'})
    else:
        return render(request, 'login.html')
    
def process_invite(request, invite_code):
    try:
        invite = Invites.objects.get(invite_code=invite_code)

        if not invite.is_valid():
            messages.error(request, "This invite link has expired or has already been used.")
            return redirect('landing_page')

        ApprovedRequest.objects.create(
            pendingRequest=PendingRequest.objects.create(
                member=request.user.member,
                sessionKey=invite.session,
                requestDate=timezone.now(),
                approvalType='approved'  # Changed from 'pending' to 'approved'
            )
        )

        # Mark invite as used
        invite.used = True
        invite.save()

        messages.success(request, "You have been successfully added to the session!")
        return redirect('session_view', session_id=invite.session.sessionKey)

    except Invites.DoesNotExist:
        messages.error(request, "Invalid invite code.")
        return redirect('landing_page')
    
def logout_view(request):
    logout(request)
    return redirect('landing_page')

def create_officer(request):
    if request.method == 'POST':
        form = OfficerForm(request.POST, request.FILES)
        if form.is_valid():
            officer = form.save(commit=False)
            officer.user = request.user
            officer.save()
            return redirect('home')
    else:
        form = OfficerForm()
    return render(request, 'create_officer.html', {'form': form})

def create_member(request):
    if request.method == 'POST':
        form = MemberForm(request.POST, request.FILES)
        if form.is_valid():
            member = form.save(commit=False)
            member.user = request.user
            member.save()
            return redirect('home')
    else:
        form = MemberForm()
    return render(request, 'create_member.html', {'form': form})

def create_guest(request):
    if request.method == 'POST':
        form = GuestForm(request.POST, request.FILES)
        if form.is_valid():
            guest = form.save(commit=False)
            guest.user = request.user
            guest.save()
            return redirect('home')
    else:
        form = GuestForm()
    return render(request, 'create_guest.html', {'form': form})

def home(request):
    user = request.user
    officer = Officer.objects.filter(user=user).first()
    member = Member.objects.filter(user=user).first()
    guest = Guest.objects.filter(user=user).first()

    if officer:
        profile = officer
    elif member:
        profile = member
    elif guest:
        profile = guest
    else:
        profile = None

    sessions = Session.objects.all()
    announcements = Announcement.objects.all()

    return render(request, 'home.html', {
        'profile': profile,
        'sessions': sessions,
        'announcements': announcements,
        'is_home_page': True,
    })

@login_required
def create_session(request):
    if request.method == 'POST':
        form = SessionForm(request.POST, request.FILES)
        if form.is_valid():
            session = form.save(commit=False)
            session.officerKey = request.user.officer
            session.save()
            return redirect('home')
    else:
        form = SessionForm()
    return render(request, 'create_session.html', {'form': form})

def join_session(request, session_id):
    session = get_object_or_404(Session, pk=session_id)
    if request.method == 'POST':
        form = RequestJoinSessionForm(request.POST)
        if form.is_valid():
            # Determine the user type and set the appropriate key
            if hasattr(request.user, 'officer'):
                user = request.user.officer.user
            elif hasattr(request.user, 'guest'):
                user = request.user.guest.user
            elif hasattr(request.user, 'member'):
                user = request.user.member.user
            else:
                # Handle the case where the user is not an officer, guest, or member
                # This might involve redirecting the user to a registration page or showing an error message
                return redirect('register')

            PendingRequest.objects.create(
                member=user.member, # Use the related User instance
                sessionKey=session,
                requestDate=form.cleaned_data['requestDate'],
                approvalType='pending'
            )
            return redirect('home')
    else:
        form = RequestJoinSessionForm()
    return render(request, 'join_session.html', {'form': form, 'session': session})

@login_required
def session_view(request, session_id):
    session = get_object_or_404(Session, pk=session_id)
    pending_requests = PendingRequest.objects.filter(sessionKey=session, approvalType='pending')
    approved_requests = ApprovedRequest.objects.filter(pendingRequest__sessionKey=session)

    pending_member_details = []
    for pending_request in pending_requests:
        member_profile = pending_request.member
        if member_profile:
            member_details = {
                'memberKey': member_profile.memberKey,
                'fname': member_profile.firstName,
                'lname': member_profile.lastName,
                'IDPicture': member_profile.IDPicture.url if member_profile.IDPicture else '',
            }
        pending_member_details.append(member_details)

    approved_member_details = []
    for approved_request in approved_requests:
        member_profile = approved_request.pendingRequest.member
        if member_profile:
            member_details = {
                'memberKey': member_profile.memberKey,
                'fname': member_profile.firstName,
                'lname': member_profile.lastName,
                'IDPicture': member_profile.IDPicture.url if member_profile.IDPicture else '',
            }
        approved_member_details.append(member_details)

    requirements = Requirement.objects.filter(session=session)  
    
    # for requirement in requirements:
    #     requirement.event_time_start_iso = requirement.deadline.isoformat()
    #     requirement.event_time_end_iso = requirement.deadline.isoformat()

    files = File.objects.filter(session=session)
    current_tab = request.GET.get('tab', 'chat')
    advisories = Advisory.objects.filter(session=session)

    pending_files = files.filter(is_approved=False)
    approved_files = files.filter(is_approved=True)

    if request.method == 'POST' and 'file' in request.FILES:
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.save(commit=False)
            file.uploaded_by = request.user
            file.session = session
            file.save()
            messages.success(request, 'File uploaded successfully!')
            return redirect('session_view', session_id=session_id)
    else:
        form = FileUploadForm()

    if request.method == 'POST' and 'message' in request.POST:
        message_text = request.POST.get('message')
        if message_text.strip():
            Message.objects.create(
                session=session,
                user=request.user,
                message=message_text
            )
            return redirect('session_view', session_id=session_id)
        
    # View Logic

    # Logic: who can access the tabs?
    show_tabs = False
    show_send_request_button = False
    show_pending_message = False
    is_officer_creator = False
    is_officer_other = False

    if hasattr(request.user, 'officer'):
        if session.officerKey == request.user.officer.officerKey:
            is_officer_creator = True
            show_tabs = True
        else:
            is_officer_other = True
            # No access for other officers
    elif hasattr(request.user, 'member'):
        member = request.user.member
        is_approved = ApprovedRequest.objects.filter(
            pendingRequest__sessionKey=session,
            pendingRequest__member=member
        ).exists()

        if is_approved:
            show_tabs = True
        else:
            has_pending = PendingRequest.objects.filter(sessionKey=session, member=member).exists()
            if has_pending:
                show_pending_message = True
            else:
                show_send_request_button = True

    context = {
        'session': session,
        'pending_requests': pending_requests,
        'approved_requests': approved_requests,
        'requirements': requirements,
        'pending_files': pending_files,
        'approved_files': approved_files,
        'current_tab': current_tab,
        'advisories': advisories,
        'form': form,
        'pending_member_details': pending_member_details,
        'approved_member_details': approved_member_details,

        # Access flags
        'show_tabs': show_tabs,
        'show_send_request_button': show_send_request_button,
        'show_pending_message': show_pending_message,
        'is_officer_creator': is_officer_creator,
        'is_officer_other': is_officer_other,
    }
    return render(request, 'session_view.html', context)

@login_required
def session_list(request):
    user_sessions = []

    if hasattr(request.user, 'member'):
        approved_requests = ApprovedRequest.objects.filter(
            pendingRequest__member=request.user.member
        ).select_related('pendingRequest__sessionKey')

        user_sessions = [ar.pendingRequest.sessionKey for ar in approved_requests]

    return render(request, 'session_list.html', {'user_sessions': user_sessions})

def mentoring_schedule(request):
    current_season = Season.objects.filter(start_year__lte=now().year, end_year__gte=now().year).first()
    if current_season:
        future_schedules = MentoringSchedule.objects.filter(seasongrouping__season=current_season, session_time__gte=now()).order_by('session_time')
        most_recent_schedule = future_schedules.first()
        schedules = MentoringSchedule.objects.filter(seasongrouping__season=current_season).order_by('session_time')
    else:
        schedules = MentoringSchedule.objects.none()
        most_recent_schedule = None

    for schedule in schedules:
        schedule.session_time_iso = schedule.session_time.isoformat()

    return render(request, 'mentoring_schedule.html', {
        'schedules': schedules,
        'current_season': current_season,
        'most_recent_schedule': most_recent_schedule,
        'most_recent_schedule_date': most_recent_schedule.session_time.strftime('%Y-%m-%d %H:%M:%S') if most_recent_schedule else '',
    })

def progress_tracking(request):
    current_season = Season.objects.filter(start_year__lte=timezone.now().year, end_year__gte=timezone.now().year).first()
    progress = ProgressTracking.objects.filter(seasongrouping__season=current_season).order_by('-progress_percentage') if current_season else ProgressTracking.objects.none()
    top_performers = TopPerformers.objects.select_related('progress_tracking').order_by('ranking')[:4]  # Top 4 spotlight

    return render(request, 'progress_tracking.html', {
        'progress': progress,
        'top_performers': top_performers,
        'current_season': current_season,
    })

def top_contributors(request):
    top_contributors = TopContributor.objects.all()
    return render(request, 'top_contributors.html', {'top_contributors': top_contributors})

# @login_required
# def profile(request):
#     user = request.user
#     officer = Officer.objects.filter(user=user).first()
#     member = Member.objects.filter(user=user).first()
#     guest = Guest.objects.filter(user=user).first()

#     if officer:
#         profile = officer
#     elif member:
#         profile = member
#     elif guest:
#         profile = guest
#     else:
#         profile = None

#     return render(request, 'profile.html', {'profile': profile})

@login_required
def profile(request):
    user = request.user
    officer = Officer.objects.filter(user=user).first()
    member = Member.objects.filter(user=user).first()
    guest = Guest.objects.filter(user=user).first()

    profile = None
    form = None

    if officer:
        profile = officer
        FormClass = OfficerEditForm
    elif member:
        profile = member
        FormClass = MemberEditForm
    elif guest:
        profile = guest
        FormClass = GuestEditForm
    else:
        profile = None
        FormClass = None

    if request.method == 'POST' and FormClass:
        form = FormClass(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('profile')
    else:
        if FormClass:
            form = FormClass(instance=profile)

    return render(request, 'profile.html', {'profile': profile, 'form': form})

def profiles(request):
    officers = Officer.objects.all()
    members = Member.objects.all()
    guests = Guest.objects.all()
    return render(request, 'profiles.html', {'officers': officers, 'members': members, 'guests': guests})

def officer_profiles(request):
    officers = Officer.objects.all()
    return render(request, 'officer_profiles.html', {'officers': officers})

def member_profiles(request):
    members = Member.objects.all()
    return render(request, 'member_profiles.html', {'members': members})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    # Fetch a random set of posts excluding the current post
    all_posts = Post.objects.exclude(pk=post.pk)
    related_posts = random.sample(list(all_posts), min(5, all_posts.count())) # Fetch 5 random posts or fewer if there are less than 5
    return render(request, 'post_detail.html', {'post': post, 'related_posts': related_posts})

def tag_posts(request, tag_name):
    tag = get_object_or_404(Tag, name=tag_name)
    posts = Post.objects.filter(tag=tag)
    return render(request, 'tag_posts.html', {'posts': posts})

def view_announcement(request, announcement_id):
    announcement = get_object_or_404(Announcement, id=announcement_id)
    comments = Comment.objects.filter(announcement=announcement)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.announcement = announcement
            comment.save()
            return redirect('view_announcement', announcement_id=announcement.id)
    else:
        form = CommentForm()

    return render(request, 'announcement_detail.html', {
        'announcement': announcement,
        'comments': comments,
        'form': form,
    })

@login_required
@require_http_methods(["GET", "POST"])
def public_forum(request):
    if request.method == "POST":
        message_text = request.POST.get("message", "").strip()
        if message_text:
            ForumMessage.objects.create(
                user=request.user,
                message=message_text,
                timestamp=timezone.now()
            )
        # No redirect for AJAX
        return JsonResponse({"status": "success"})

    # If GET with AJAX polling
    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        since = request.GET.get("since")
        messages = ForumMessage.objects.all().order_by("timestamp")
        if since:
            try:
                since = since.replace(' ', '+')
                since_dt = date_parser.isoparse(since)
                messages = messages.filter(timestamp__gt=since_dt)
            except (ValueError, TypeError):
                # Fallback: just return the last 50 messages
                messages = messages.order_by("-timestamp")[:50]

        data = [
            {
                "user": m.user.username,
                "message": m.message,
                "timestamp": m.timestamp.isoformat()
            }
            for m in messages
        ]
        return JsonResponse(data, safe=False)

    # Normal render
    messages = ForumMessage.objects.all().order_by("timestamp")
    return render(request, "public_forum.html", {"messages": messages})


def helpdesk(request):
    admin_user = User.objects.filter(is_superuser=True).first()
    if not admin_user:
        return JsonResponse({"error": "No admin user found."}, status=404)

    if request.method == "POST" and request.is_ajax():
        msg = request.POST.get("message")
        HelpdeskMessage.objects.create(
            sender=request.user,
            recipient=admin_user,
            message=msg,
            is_from_admin=False
        )
        return JsonResponse({"status": "Message sent."})

    # Get all messages between user and admin
    messages = HelpdeskMessage.objects.filter(
        sender=request.user, recipient=admin_user
    ) | HelpdeskMessage.objects.filter(
        sender=admin_user, recipient=request.user
    )
    messages = messages.order_by("timestamp")

    return render(request, "helpdesk_chat.html", {"messages": messages})

def helpdesk_send(request):
    if request.method == "POST" and request.user.is_authenticated:
        message_text = request.POST.get("message", "").strip()
        if message_text:
            admin_user = User.objects.filter(is_superuser=True).first()
            HelpdeskMessage.objects.create(
                sender=request.user,
                recipient=admin_user,
                message=message_text,
                timestamp=timezone.now(),
                is_from_admin=False
            )
            return JsonResponse({"status": "sent"})
    return JsonResponse({"status": "error"})

def helpdesk_messages(request):
    if not request.user.is_authenticated:
        return JsonResponse([], safe=False)

    since = request.GET.get("since")
    messages = HelpdeskMessage.objects.filter(Q(sender=request.user) | Q(recipient=request.user)).order_by("timestamp")
    messages = messages.order_by("timestamp")

    if since:
        try:
            since_dt = parse_datetime(since)
            if since_dt:
                messages = messages.filter(timestamp__gt=since_dt)
        except:
            pass

    data = [{
        "id": msg.id,
        "user": msg.sender.username,
        "message": msg.message,
        "timestamp": msg.timestamp.isoformat(),
        "is_admin": msg.is_from_admin
    } for msg in messages]

    return JsonResponse(data, safe=False)

def resource_list(request):
    resources = Resource.objects.all()
    return render(request, 'resource_list.html', {'resources': resources})

def experts_by_resource(request, resource_id):
    resource = get_object_or_404(Resource, id=resource_id)
    experts = resource.experts.all()
    return render(request, 'experts_by_resource.html', {'resource': resource, 'experts': experts})

def expert_detail(request, expert_id):
    expert = get_object_or_404(Expert, id=expert_id)
    return render(request, 'expert_detail.html', {'expert': expert})

@login_required
def connect_to_expert(request, expert_id):
    expert = get_object_or_404(Expert, id=expert_id)
    if expert.user:
        if request.method == 'POST':
            form = CorrespondenceForm(request.POST, request.FILES)
            if form.is_valid():
                correspondence = form.save(commit=False)
                correspondence.sender = request.user
                correspondence.recipient = expert.user
                correspondence.save()
                return redirect('inbox')
        else:
            form = CorrespondenceForm()
        return render(request, 'connect_form.html', {'form': form, 'expert': expert})

@login_required
def inbox(request):
    # Get all messages where user is sender or recipient
    all_messages = Correspondence.objects.filter(
        models.Q(sender=request.user) | models.Q(recipient=request.user)
    ).select_related('recipient', 'sender')

    threads = defaultdict(list)

    for msg in all_messages:
        # The other participant in the conversation
        other_user = msg.recipient if msg.recipient != request.user else msg.sender
        threads[other_user].append(msg)

    # Pass dict for easy iteration in template
    return render(request, "inbox.html", {'threads': dict(threads), 'user': request.user})

@require_POST
@login_required
def send_correspondence(request):
    subject = request.POST.get('subject')
    body = request.POST.get('body')
    recipient_username = request.POST.get('recipient_username')
    image = request.FILES.get('image')

    if not recipient_username:
        return HttpResponseBadRequest("Recipient username is required")

    recipient = get_object_or_404(User, username=recipient_username)

    Correspondence.objects.create(
        subject=subject,
        body=body,
        recipient=recipient,
        sender=request.user,
        image=image
    )

    return redirect('inbox')

@require_POST
@login_required
def mark_as_read(request, msg_id):
    try:
        msg = Correspondence.objects.get(id=msg_id, recipient=request.user)
        msg.is_read = True
        msg.save()
        return JsonResponse({'status': 'success'})
    except Correspondence.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Message not found or unauthorized'}, status=404)