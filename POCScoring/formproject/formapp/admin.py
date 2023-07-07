from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from .models import Form, Employee, Section, Subsection, Question, Response, FormAssignment
# other imports...

class FormAdmin(admin.ModelAdmin):
    list_display = ('title', 'creator', 'creation_date', 'delete_button')

    def delete_button(self, obj):
        return format_html('<a class="btn" href="{}">Delete</a>', reverse('admin:delete_form', args=[obj.pk]))

    delete_button.short_description = 'Delete Form'
    delete_button.allow_tags = True

admin.site.register(Form, FormAdmin)
admin.site.register(Employee)
admin.site.register(Section)
admin.site.register(Subsection)
admin.site.register(Question)
admin.site.register(Response)
admin.site.register(FormAssignment)
# other admin.site.register() calls...
