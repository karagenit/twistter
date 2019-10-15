from django.contrib import admin

from .models import User, Post, Tag, Follow, Report

admin.site.register(User)
admin.site.register(Post)
admin.site.register(Tag)
admin.site.register(Follow)

def delete_reported_post(modeladmin, request, queryset):
    for report in queryset:
        report.post.delete()
        report.delete()

class ReportAdmin(admin.ModelAdmin):
    list_display = ['get_post_content', 'get_post_author'] # TODO: Display post name & user?
    actions = [delete_reported_post]

    def get_post_content(self, report):
        return report.post.content
    get_post_content.short_description = 'Post Content'

    def get_post_author(self, report):
        return report.post.creator.firstname + ' ' + report.post.creator.lastname
    get_post_author.short_description = 'Poster'

admin.site.register(Report, ReportAdmin)
