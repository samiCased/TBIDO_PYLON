from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *

class CustomUserCreationForm(UserCreationForm):
    user_type = forms.ChoiceField(
        choices=[
            ('officer', 'Officer'),
            ('member', 'Member'),  # Changed from 'player'
            ('guest', 'Guest'),
        ],
        widget=forms.Select(attrs={'placeholder': 'Select user type'}),
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('user_type',)
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Enter your username'}),
            'password1': forms.PasswordInput(attrs={'placeholder': 'Enter your password'}),
            'password2': forms.PasswordInput(attrs={'placeholder': 'Confirm your password'}),
        }

class CandidateForm(forms.ModelForm):
    class Meta:
        model = Candidate
        fields = ['name', 'id_picture', 'age', 'employment', 'height', 'rank', 'employee_number', 'amount_paid']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Surname, First Name, M.I.'}),
            'employment': forms.TextInput(attrs={'placeholder': 'Type "Yes", "No", or "To Apply"'}),
            'height': forms.TextInput(attrs={'placeholder': 'E.g.: 5-11'}),
            'rank': forms.TextInput(attrs={'placeholder': 'Enter rank number (1-5)'}),
            'employee_number': forms.TextInput(attrs={'placeholder': 'Enter employee/student number'}),
            'amount_paid': forms.TextInput(attrs={'placeholder': 'IN PHP; (E.g.: 350)'}),
        }

class OfficerForm(forms.ModelForm):
    employmentDate = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'placeholder': 'Enter officer employment date'}))

    class Meta:
        model = Officer
        exclude = ['user', 'status']

class MemberForm(forms.ModelForm):
    employmentDate = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'placeholder': 'Enter member employment date'}))

    class Meta:
        model = Member
        exclude = ['user', 'status']

class GuestForm(forms.ModelForm):
    employmentDate = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'placeholder': 'Enter guest employment date'}))

    class Meta:
        model = Guest
        exclude = ['user', 'status']

class SessionForm(forms.ModelForm):
    class Meta:
        model = Session
        fields = ['banner', 'sessionDateKey', 'sessionTimeKey', 'membershipTypeKey', 'sessionStatus', 'sessionMaterialCovered']
        exclude = ['officerKey']
        widgets = {
            'sessionDateKey': forms.DateInput(attrs={'type': 'date', 'placeholder': 'Enter session date'}),
            'sessionTimeKey': forms.TimeInput(attrs={'type': 'time', 'placeholder': 'Enter session time'}),
        }

class OfficerEditForm(forms.ModelForm):
    class Meta:
        model = Officer
        exclude = ['user', 'officerKey']
        widgets = {
            'employmentDate': forms.DateInput(attrs={
                'type': 'date', 
                'class': 'custom-date-input'
            }),
            'IDPicture': forms.ClearableFileInput(attrs={
                'class': 'custom-file-input'
            }),
            'pictureFullBody': forms.ClearableFileInput(attrs={
                'class': 'custom-file-input'
            }),
            # For other text fields, add class in your template or via widget attrs if you want
        }

class MemberEditForm(forms.ModelForm):
    class Meta:
        model = Member
        exclude = ['user', 'memberKey']
        widgets = {
            'employmentDate': forms.DateInput(attrs={
                'type': 'date', 
                'class': 'custom-date-input'
            }),
            'IDPicture': forms.ClearableFileInput(attrs={
                'class': 'custom-file-input'
            }),
            'pictureFullBody': forms.ClearableFileInput(attrs={
                'class': 'custom-file-input'
            }),
        }

class GuestEditForm(forms.ModelForm):
    class Meta:
        model = Guest
        exclude = ['user', 'guestKey']
        widgets = {
            'employmentDate': forms.DateInput(attrs={
                'type': 'date', 
                'class': 'custom-date-input'
            }),
            'IDPicture': forms.ClearableFileInput(attrs={
                'class': 'custom-file-input'
            }),
            'pictureFullBody': forms.ClearableFileInput(attrs={
                'class': 'custom-file-input'
            }),
        }

# class OfficerEditForm(forms.ModelForm):
#     class Meta:
#         model = Officer
#         exclude = ['user', 'officerKey']
#         widgets = {
#             'employmentDate': forms.DateInput(attrs={'type': 'date'}),
#             'IDPicture': forms.ClearableFileInput(),
#             'pictureFullBody': forms.ClearableFileInput(),
#         }

# class MemberEditForm(forms.ModelForm):
#     class Meta:
#         model = Member
#         exclude = ['user', 'memberKey']
#         widgets = {
#             'employmentDate': forms.DateInput(attrs={'type': 'date'}),
#             'IDPicture': forms.ClearableFileInput(),
#             'pictureFullBody': forms.ClearableFileInput(),
#         }

# class GuestEditForm(forms.ModelForm):
#     class Meta:
#         model = Guest
#         exclude = ['user', 'guestKey']
#         widgets = {
#             'employmentDate': forms.DateInput(attrs={'type': 'date'}),
#             'IDPicture': forms.ClearableFileInput(),
#             'pictureFullBody': forms.ClearableFileInput(),
#         }

class RequestJoinSessionForm(forms.ModelForm):
    class Meta:
        model = Request
        fields = ['membershipTypeKey', 'requestDate']
        widgets = {
            'requestDate': forms.DateInput(attrs={'type': 'date', 'placeholder': 'Enter request date'}),
        }

class FileUploadForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ('file', 'requirement')
        widgets = {
            'file': forms.FileInput(attrs={'class': 'form-control'}),
            'requirement': forms.Select(attrs={'class': 'form-control'})
        }

class PendingRequestForm(forms.ModelForm):
    class Meta:
        model = PendingRequest
        fields = '__all__'
        widgets = {
            'approvalType': forms.Select(choices=[
                ('pending', 'Pending'),
                ('approved', 'Approved'),
            ]),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']

class CorrespondenceForm(forms.ModelForm):
    class Meta:
        model = Correspondence
        fields = ['subject', 'image', 'body']
        widgets = {
            'subject': forms.TextInput(attrs={'placeholder': 'What is the subject of your inquiry?'}),
        }

# class PostAdminForm(forms.ModelForm):
#     content = forms.CharField(widget=CKEditorUploadingWidget())
#     class Meta:
#         model = Post
#         fields = '__all__'

# class VideoPostAdminForm(forms.ModelForm):
#     content = forms.CharField(widget=CKEditorUploadingWidget())
#     class Meta:
#         model = VideoPost
#         fields = '__all__'

# class SponsorPostAdminForm(forms.ModelForm):
#     content = forms.CharField(widget=CKEditorUploadingWidget())
#     class Meta:
#         model = SponsorPost
#         fields = '__all__'