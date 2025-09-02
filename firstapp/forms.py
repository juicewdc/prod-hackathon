from .models import ProjectUser
from django.contrib.auth.forms import UserCreationForm


class ProjectUserRegisterForm(UserCreationForm):
    class Meta:
        model = ProjectUser
        fields = (
                'username', 'email', 'password1', 'password2')
