from django.contrib import admin
from web import models

# Register your models here.
admin.site.register(models.UserInfo)
admin.site.register(models.Note)
admin.site.register(models.NoteComment)
admin.site.register(models.TBicture)
admin.site.register(models.NoteCollection)