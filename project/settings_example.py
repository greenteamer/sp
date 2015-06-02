import os
# File for storing custom settings
CURRPATH = os.path.abspath('.')
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'sp',
        'USER': 'root',
        'PASSWORD': 'balabas',
        'HOST': '',
        'PORT': '',
        'TEST_CHARSET': 'UTF8',
    }
}

# DEBUG_TOOLBAR_PATCH_SETTINGS = False

ADMIN_EMAIL = 'greenteamer@bk.ru'
ACCOUNT_ACTIVATION_DAYS = 2

CKEDITOR_UPLOAD_PATH = "uploads/"
CKEDITOR_JQUERY_URL = '//ajax.googleapis.com/ajax/libs/jquery/2.1.1/jquery.min.js'
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': [
            ['Source', '-', 'Save', 'NewPage', 'DocProps',
                'Preview', 'Print', '-', 'Templates'],

            ['Cut', 'Copy', 'Paste', 'PasteText', 'PasteFromWord',
                '-', 'Undo', 'Redo'],

            ['Find', 'Replace', '-', 'SelectAll', '-', 'SpellChecker'],
            ['Image', 'Table', 'HorizontalRule', 'Smiley', 'SpecialChar'],
            ['Bold', 'Italic', 'Underline', 'Strike', 'Subscript',
                'Superscript', '-', 'RemoveFormat'],

            ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-',
                'Blockquote', '-', 'JustifyLeft', 'JustifyCenter',
                'JustifyRight', 'JustifyBlock', '-', 'BidiLtr', 'BidiRtl'],

            ['Link', 'Unlink'],
            ['Styles', 'Format', 'Font', 'FontSize'],
            ['TextColor', 'BGColor'],
            ['Maximize', 'ShowBlocks', 'CreateDiv'],
        ],
        'width': 1040,
        'height': 500,
    },
    'interface': {
        'toolbar': [
            ['Source', '-', 'Save', 'NewPage', 'DocProps',
                'Preview', 'Print', '-', 'Templates'],

            ['Cut', 'Copy', 'Paste', 'PasteText', 'PasteFromWord',
                '-', 'Undo', 'Redo'],

            ['Find', 'Replace', '-', 'SelectAll', '-', 'SpellChecker'],
            ['Image', 'Table', 'HorizontalRule', 'Smiley', 'SpecialChar'],
            ['Bold', 'Italic', 'Underline', 'Strike', 'Subscript',
                'Superscript', '-', 'RemoveFormat'],

            ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-',
                'Blockquote', '-', 'JustifyLeft', 'JustifyCenter',
                'JustifyRight', 'JustifyBlock', '-', 'BidiLtr', 'BidiRtl'],

            ['Link', 'Unlink'],
            ['Styles', 'Format', 'Font', 'FontSize'],
            ['TextColor', 'BGColor'],
            ['Maximize', 'ShowBlocks', 'CreateDiv'],
        ],
        'width': 775,
        'height': 500,
    },
}

AUTH_USER_EMAIL_UNIQUE = True
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'teamer777@gmail.com'
EMAIL_HOST_PASSWORD = 'greenteamer1986'
EMAIL_PORT = 587
