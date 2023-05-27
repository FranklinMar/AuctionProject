from django.forms import Form, FileField, FileInput


class UploadFileForm(Form):
    file = FileField(allow_empty_file=True, widget=FileInput(attrs={
                'style': 'display: contents;',
                'accept': '.jpg, .svg, .png, .gif',
                'id': 'file'
            }))
