from django.contrib import admin

from .models import User, Post, Tag, Follow, Report

from datetime import date, timedelta

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

def temp_ban_user(modeladmin, request, queryset):
    queryset.update(banned_until = date.today() + timedelta(days=7))

def verify_user(modeladmin, request, queryset):
    queryset.update(verified = 2)

class UserAdmin(admin.ModelAdmin):
    list_display = ['firstname', 'lastname']
    actions = [temp_ban_user, verify_user]

admin.site.register(User, UserAdmin)
