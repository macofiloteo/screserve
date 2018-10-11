from django import forms
from .models import Profile
from django.contrib.auth.models import User
from django.core.files.images import get_image_dimensions

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('avatar','fname','mname','lname','contact', 'sex','address', 'birthday')

###https://stackoverflow.com/questions/6396442/add-image-avatar-field-to-users-in-django
    def clean_avatar(self):
        avatar = self.cleaned_data['avatar']
        try:
            w, h = get_image_dimensions(avatar)
            print(w)
            print(h)
            #validate dimensions
            max_width = max_height = 500
            if w > max_width or h > max_height:
                raise forms.ValidationError(
                    u'Please use an image that is '
                     '%s x %s pixels or smaller.' % (max_width, max_height))

            #validate content type
                main, sub = avatar.content_type.split('/')
                if not (main == 'image' and sub in ['jpeg', 'pjpeg', 'gif', 'png', 'jpg']):
                    raise forms.ValidationError(u'Please use a JPEG, '
                        'GIF or PNG image.')


            #validate file size
            if len(avatar) > (20 * 1024):
                raise forms.ValidationError(
                    u'Avatar file size may not exceed 20k.')

        except TypeError:
            """
            Handles case when we are updating the user profile
            and do not supply a new avatar
            """
            pass
        return avatar
###https://stackoverflow.com/questions/6396442/add-image-avatar-field-to-users-in-django

class OfficerForm(forms.ModelForm):
    groups = forms.CharField(max_length=15)
    class Meta:
        model = User
        fields = ('username', 'password')
