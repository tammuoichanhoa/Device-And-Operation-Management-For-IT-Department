from django.contrib import admin
from common.models import *
from common.admin import *
from .models import *
from mptt.admin import DraggableMPTTAdmin

# Register your models here.

@admin.register(OutgoingDocuments)
class OutgoingDocumentsAdmin(BaseDocumentsAdmin):
    list_per_page = 20
    list_display = ('get_ms_display', 'document_type', 'date', 'title', 'security', 'display_destination')
    filter_horizontal = ('destination', 'receiver')
    
    def get_fieldsets(self, request, obj=None):
        """Thêm nhóm thông tin về nơi nhận"""
        fieldsets = super().get_fieldsets(request, obj)
        outgoing_fieldsets = fieldsets + (
            ('Thông tin nơi nhận', {
                'fields': ('destination', 'receiver')
            }),
        )
        return outgoing_fieldsets
    
    def display_destination(self, obj):
        """Hiển thị tóm tắt các nơi nhận"""
        destinations = list(obj.destination.all())
        if not destinations:
            return '—'
        elif len(destinations) <= 2:
            return ', '.join(d.name for d in destinations)
        else:
            return f'{destinations[0].name}, {destinations[1].name}... (+{len(destinations)-2})'
    
    display_destination.short_description = 'Nơi nhận'


@admin.register(IncomingDocuments)
class IncomingDocumentsAdmin(BaseDocumentsAdmin):
    list_per_page = 20
    list_display = ('get_ms_display', 'document_type', 'date', 'title', 'security', 'display_source')
    filter_horizontal = ('source', 'sender')
    
    def get_fieldsets(self, request, obj=None):
        """Thêm nhóm thông tin về nơi gửi"""
        fieldsets = super().get_fieldsets(request, obj)
        incoming_fieldsets = fieldsets + (
            ('Thông tin nơi gửi', {
                'fields': ('source', 'sender')
            }),
        )
        return incoming_fieldsets
    
    def display_source(self, obj):
        """Hiển thị tóm tắt các nơi gửi"""
        sources = list(obj.source.all())
        if not sources:
            return '—'
        elif len(sources) <= 2:
            return ', '.join(s.name for s in sources)
        else:
            return f'{sources[0].name}, {sources[1].name}... (+{len(sources)-2})'
    
    display_source.short_description = 'Nơi gửi'
