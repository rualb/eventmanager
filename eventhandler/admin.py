from django.contrib import admin

# Register your models here.

from .forms import EventRecordForm
from .models import EventRecord,EventType
  
#admin.site.register( EventRecord, EventRecordAdmin)
@admin.register(EventRecord)
class EventRecordAdmin(admin.ModelAdmin):
    #search_fields = ['textf1' ]
    #form = EventRecordForm
    pass

@admin.register(EventType)
class EventTypeAdmin(admin.ModelAdmin):
    pass

