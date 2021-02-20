from django.db import models
import os
def content_file_name(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s_%s.%s" % (instance.user.id, instance.questid.id, ext)
    return os.path.join('uploads', filename)
    
class Document(models.Model):
    user = models.UUIDField(null=False, unique=False)
    vid = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return str(self.uploaded_at)
# Create your models here.
