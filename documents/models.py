from django.db import models
from common.models import *
from django.utils.timezone import now

# Create your models here.

# ========================================================================================================================
#                                                Quản lý công văn
# ========================================================================================================================
class OutgoingDocuments(BaseDocument):
    class Meta:
        db_table = 'outgoing_documents'
        verbose_name = 'Quản lý văn bản đi'
        verbose_name_plural = 'Văn bản đi'
    
    destination = models.ManyToManyField(Department, blank=True, verbose_name='Cơ quan nhận', related_name="docs_destination")
    receiver = models.ManyToManyField(Staff, blank=True, verbose_name="Người nhận", related_name="docs_receiver")
    
    @classmethod
    def get_next_id(cls):
        """Lấy ID tiếp theo cho văn bản đi"""
        current_year = now().year
        latest_doc = cls.objects.filter(date__year=current_year).order_by('-id').first()
        return 1 if not latest_doc else latest_doc.id + 1
    
    def save(self, *args, **kwargs):
        if not self.ms and self.document_type:
            doc_id = self.get_next_id()
            self.ms = f"{doc_id}/{self.document_type.id}-BD{now().year}"
        super().save(*args, **kwargs)

class IncomingDocuments(BaseDocument):
    class Meta:
        db_table = 'incoming_documents'
        verbose_name = 'Quản lý văn bản đến'
        verbose_name_plural = 'Văn bản đến'
    
    source = models.ManyToManyField(Department, blank=True, verbose_name='Cơ quan gửi', related_name="docs_source")
    sender = models.ManyToManyField(Staff, blank=True, verbose_name="Người gửi", related_name="docs_sender")
    
    @classmethod
    def get_next_id(cls):
        """Lấy ID tiếp theo cho văn bản đến"""
        current_year = now().year
        latest_doc = cls.objects.filter(date__year=current_year).order_by('-id').first()
        return 1 if not latest_doc else latest_doc.id + 1
    
    def save(self, *args, **kwargs):
        if not self.ms and self.document_type:
            doc_id = self.get_next_id()
            self.ms = f"{doc_id}/{self.document_type.id}{now().year}"
        super().save(*args, **kwargs)

