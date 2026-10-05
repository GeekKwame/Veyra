from django.contrib import admin
from .models import Career, CompetencyArea, Skill, SkillPrerequisite, Topic, Resource

class CompetencyAreaInline(admin.TabularInline):
    model = CompetencyArea
    extra = 1

class SkillInline(admin.TabularInline):
    model = Skill
    extra = 1
    fields = ('title', 'slug', 'taxonomy', 'estimated_hours')

class SkillPrerequisiteInline(admin.TabularInline):
    model = SkillPrerequisite
    fk_name = 'skill'
    extra = 1

class TopicInline(admin.TabularInline):
    model = Topic
    extra = 1

class ResourceInline(admin.TabularInline):
    model = Resource
    extra = 1
    fields = ('title', 'provider_name', 'resource_type', 'estimated_minutes', 'verification_status', 'url')

@admin.register(Career)
class CareerAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'industry_category', 'avg_months_to_complete', 'badge', 'is_published')
    list_filter = ('industry_category', 'is_published')
    search_fields = ('title', 'description', 'industry_category')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [CompetencyAreaInline]

@admin.register(CompetencyArea)
class CompetencyAreaAdmin(admin.ModelAdmin):
    list_display = ('title', 'career', 'sort_order')
    list_filter = ('career',)
    search_fields = ('title', 'career__title')
    inlines = [SkillInline]

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('title', 'competency_area', 'taxonomy', 'estimated_hours')
    list_filter = ('taxonomy', 'competency_area__career')
    search_fields = ('title', 'description')
    inlines = [SkillPrerequisiteInline, TopicInline]

@admin.register(SkillPrerequisite)
class SkillPrerequisiteAdmin(admin.ModelAdmin):
    list_display = ('prerequisite_skill', 'skill', 'is_strict')
    list_filter = ('is_strict', 'skill__competency_area__career')
    search_fields = ('skill__title', 'prerequisite_skill__title')

@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('title', 'skill', 'sort_order')
    list_filter = ('skill__competency_area__career',)
    search_fields = ('title', 'description')
    inlines = [ResourceInline]

@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ('title', 'provider_name', 'resource_type', 'estimated_minutes', 'is_completely_free', 'verification_status', 'last_verified_at')
    list_filter = ('verification_status', 'resource_type', 'is_completely_free')
    search_fields = ('title', 'url', 'provider_name')
    actions = ['mark_as_published', 'mark_as_degraded']

    @admin.action(description="Mark selected resources as PUBLISHED")
    def mark_as_published(self, request, queryset):
        queryset.update(verification_status='PUBLISHED')

    @admin.action(description="Mark selected resources as DEGRADED")
    def mark_as_degraded(self, request, queryset):
        queryset.update(verification_status='DEGRADED')
