import os
# File for storing custom settings
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'waymy',                      # Or path to database file if using sqlite3.
        'USER': 'root',                      # Not used with sqlite3.
        'PASSWORD': 'balabas',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
        # 'TEST_CHARSET': 'UTF-8',
    }
}

ADMIN_EMAIL = 'greenteamer@bk.ru'
ACCOUNT_ACTIVATION_DAYS = 2

# # CKEDITOR_MEDIA_PREFIX  = "/media/ckeditor/"
# CKEDITOR_UPLOAD_PATH = "/Users/greenteamer/Desktop/Django/applications/tai/webshop/static/uploads"
# CKEDITOR_UPLOAD_PREFIX = "/static/uploads"
# CKEDITOR_CONFIGS = {
#     'default': {
#         'toolbar': 'Base',
#     },
# }
CKEDITOR_UPLOAD_PATH = "uploads/"
CKEDITOR_JQUERY_URL = '//ajax.googleapis.com/ajax/libs/jquery/2.1.1/jquery.min.js'
CKEDITOR_CONFIGS = {
            'default': {
                # 'toolbar': 'Full',
                'toolbar': [
                    [ 'Source','-','Save','NewPage','DocProps','Preview','Print','-','Templates' ],
                    [ 'Cut','Copy','Paste','PasteText','PasteFromWord','-','Undo','Redo' ],
                    [ 'Find','Replace','-','SelectAll','-','SpellChecker'],
                    [ 'Image','Table','HorizontalRule','Smiley','SpecialChar' ],
                    # '/',
                    [ 'Bold','Italic','Underline','Strike','Subscript','Superscript','-','RemoveFormat' ],
                    [ 'NumberedList','BulletedList','-','Outdent','Indent','-','Blockquote','-','JustifyLeft','JustifyCenter','JustifyRight','JustifyBlock','-','BidiLtr','BidiRtl' ],
                    [ 'Link','Unlink' ],
                    # '/',
                    [ 'Styles','Format','Font','FontSize' ],
                    [ 'TextColor','BGColor' ],
                    [ 'Maximize', 'ShowBlocks', 'CreateDiv' ],
                ],
                'width': 1040,
                'height': 500,
            }
       }

# CKEDITOR.editorConfig = function( config ) {
#     config.toolbar_Full = [
#         { name: 'document', items : [ 'Source','-','Save','NewPage','DocProps','Preview','Print','-','Templates' ] },
#         { name: 'clipboard', items : [ 'Cut','Copy','Paste','PasteText','PasteFromWord','-','Undo','Redo' ] },
#         { name: 'editing', items : [ 'Find','Replace','-','SelectAll','-','SpellChecker', 'Scayt' ] },
#         { name: 'forms', items : [ 'Form', 'Checkbox', 'Radio', 'TextField', 'Textarea', 'Select', 'Button', 'ImageButton', 'HiddenField' ] },
#     '/',
#         { name: 'basicstyles', items : [ 'Bold','Italic','Underline','Strike','Subscript','Superscript','-','RemoveFormat' ] },
#         { name: 'paragraph', items : [ 'NumberedList','BulletedList','-','Outdent','Indent','-','Blockquote','CreateDiv','-','JustifyLeft','JustifyCenter','JustifyRight','JustifyBlock','-','BidiLtr','BidiRtl' ] },
#         { name: 'links', items : [ 'Link','Unlink','Anchor' ] },
#         { name: 'insert', items : [ 'Image','Flash','Table','HorizontalRule','Smiley','SpecialChar','PageBreak' ] },
#     '/',
#         { name: 'styles', items : [ 'Styles','Format','Font','FontSize' ] },
#         { name: 'colors', items : [ 'TextColor','BGColor' ] },
#         { name: 'tools', items : [ 'Maximize', 'ShowBlocks','-','About' ] }
#     ];
# };


AUTH_USER_EMAIL_UNIQUE = True
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'teamer777@gmail.com'
EMAIL_HOST_PASSWORD = 'greenteamer1986'
EMAIL_PORT = 587

