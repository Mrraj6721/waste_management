from django.contrib import admin
from .models import Report
from django.utils.html import format_html
from django.utils.safestring import mark_safe

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('id', 'image_tag', 'waste_type', 'severity', 'status', 'confidence', 'reported_at', 'address_preview')
    list_filter = ('waste_type', 'severity', 'status', 'detected', 'notified_authorities', 'reported_at')
    list_editable = ('status', 'severity')
    readonly_fields = ('image_tag', 'reported_at', 'updated_at', 'confidence', 'detected', 'waste_type')
    search_fields = ('address', 'description', 'reported_by__username')
    date_hierarchy = 'reported_at'
    
    fieldsets = (
        ('Report Information', {
            'fields': ('image', 'image_tag', 'description', 'severity', 'status')
        }),
        ('Location', {
            'fields': ('location_lat', 'location_lng', 'address')
        }),
        ('AI Detection Results', {
            'fields': ('detected', 'confidence', 'waste_type')
        }),
        ('Tracking', {
            'fields': ('reported_by', 'reported_at', 'updated_at')
        }),
        ('Authority Notification', {
            'fields': ('notified_authorities', 'authority_response')
        }),
    )

    def image_tag(self, obj):
        if obj.image:
            return format_html(
                '<a href="{}" target="_blank"><img src="{}" style="max-height: 200px; max-width: 200px; border: 1px solid #ccc;" /></a>',
                obj.image.url, obj.image.url
            )
        return "No Image"
    image_tag.short_description = 'Image'
    
    def address_preview(self, obj):
        if obj.address:
            return obj.address[:50] + '...' if len(obj.address) > 50 else obj.address
        return f"{obj.location_lat:.4f}, {obj.location_lng:.4f}"
    address_preview.short_description = 'Location'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('reported_by')
    
    actions = ['mark_as_confirmed', 'mark_as_resolved', 'notify_authorities_manual']
    
    def mark_as_confirmed(self, request, queryset):
        queryset.update(status='confirmed')
    mark_as_confirmed.short_description = "Mark selected reports as confirmed"
    
    def mark_as_resolved(self, request, queryset):
        queryset.update(status='resolved')
    mark_as_resolved.short_description = "Mark selected reports as resolved"
    
    def notify_authorities_manual(self, request, queryset):
        from .views import notify_authorities
        for report in queryset:
            notify_authorities(report)
            report.notified_authorities = True
            report.save()
    notify_authorities_manual.short_description = "Notify authorities for selected reports"