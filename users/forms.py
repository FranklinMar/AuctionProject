from django.forms import Form, CharField, PasswordInput, EmailInput, ImageField, FileInput


class ChangeEmail(Form):
    email = CharField(label='Email Address', widget=EmailInput(attrs={
        'class': 'form-control bg-transparent text-white form-control-sm',
        'placeholder': 'Email',
        'style': 'display: none'
    }))


class ChangePassword(Form):
    password = CharField(label='Password', widget=PasswordInput(attrs={
        'class': 'mb-2 bg-dark text-white form-control form-control-sm',
        'placeholder': 'Password',
        'style': 'display: none'
    }))


class ChangeImage(Form):
    image = ImageField(label='Image', widget=FileInput(attrs={
        'class': 'form-control bg-dark text-white form-control-sm mt-2 mb-2',
        'style': 'width: 100%; max-width: 1000px'
    }))
    # image = FileField(allow_empty_file=False, widget=FileInput(attrs={
    #             'accept': '.jpg, .svg, .png, .gif',
    #             'id': 'file'
    #         }))
