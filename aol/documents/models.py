from django.core.urlresolvers import reverse
from django.contrib.gis.db import models
from aol.lakes.models import NHDLake

class Document(models.Model):
    """
    Stores all the documents attached to a lake like PDFs, and whatever else an
    admin wants to upload (except Photos which are handled in their own model)
    """
    DOCUMENT_DIR = "pages/"
    # doc types
    OTHER = 0
    MAP = 1

    document_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to=lambda instance, filename: instance.DOCUMENT_DIR + filename)
    rank = models.IntegerField(verbose_name="Weight", help_text="Defines the order in which items are listed.")
    uploaded_on = models.DateTimeField(auto_now_add=True)
    type = models.IntegerField(choices=(
        (OTHER, "Other"),
        (MAP, "Map"),
    ), help_text="Map documents will appear on the 'Maps' tab on the lake page")
    friendly_filename = models.CharField(max_length=255, blank=True)

    lake = models.ForeignKey(NHDLake, db_column="reachcode")

    class Meta:
        db_table = 'document'
        ordering = ['rank']


    @property
    def url(self):
        return reverse("documents-download", args=(self.pk,))
