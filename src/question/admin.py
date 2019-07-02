from django.contrib import admin

from question import models


admin.site.register(models.QuestionTag)
admin.site.register(models.TaggedQuestion)
admin.site.register(models.Question)
admin.site.register(models.Answer)
admin.site.register(models.Comment)
