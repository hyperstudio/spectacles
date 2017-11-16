import datetime
from haystack import indexes
from datastore.models import Document
from datastore.models import Annotation


#class Note(models.Model):
#    user = models.ForeignKey(User)
#    pub_date = models.DateTimeField()
#    title = models.CharField(max_length=200)
#    body = models.TextField()

class DocumentIndex(indexes.SearchIndex, indexes.Indexable):
    # Text
    # Title
    # Author
    text = indexes.CharField(document=True, use_template=True)

    created_at = indexes.DateTimeField(model_attr='created_at')
    updated_at = indexes.DateTimeField(model_attr='updated_at')
    creator = indexes.CharField(model_attr='creator')

    def get_model(self):
        return Document

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()


class AnnotationIndex(indexes.SearchIndex, indexes.Indexable):
    # data['quote']
    # data['text']
    text = indexes.CharField(document=True, use_template=True)

    created_at = indexes.DateTimeField(model_attr='created_at')
    updated_at = indexes.DateTimeField(model_attr='updated_at')
    creator = indexes.CharField(model_attr='creator')
    uuid = indexes.CharField(model_attr='uuid')
    tags = indexes.MultiValueField()

    def get_model(self):
        return Annotation

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()

    def prepare_tags(self, obj):
        return obj.tags
