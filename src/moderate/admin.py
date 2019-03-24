from django.contrib import admin

from moderate import models

admin.site.register(models.Report)
admin.site.register(models.ReportComment)
