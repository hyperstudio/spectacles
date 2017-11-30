from django_elasticsearch_dsl import DocType, Index, fields
from datastore.models import Annotation
from datastore.models import Document
from django.conf import settings


document_index = Index('spectacles-document')
document_index.settings(
    number_of_shards=1,
    number_of_replicas=0
)
@document_index.doc_type
class ESDocument(DocType):
    id = fields.IntegerField(attr='id')
    creator = fields.ObjectField(properties={
        'email': fields.TextField(),
        'name': fields.TextField(),
    })
    text = fields.TextField(attr='text')
    title = fields.TextField(attr='title')
    author = fields.TextField(attr='author')
    created_at = fields.DateField(attr='created_at')
    updated_at = fields.DateField(attr='updated_at')

    class Meta:
        model = Document
        ignore_signals = settings.ES_IGNORE_SIGNALS
        auto_refresh = settings.ES_AUTO_REFRESH


annotation_index = Index('spectacles-annotation')
annotation_index.settings(
    number_of_shards=1,
    number_of_replicas=0
)
@annotation_index.doc_type
class ESAnnotation(DocType):
    uuid = fields.TextField(attr='uuid')
    creator = fields.ObjectField(properties={
        'email': fields.TextField(),
        'name': fields.TextField(),
    })
    created_at = fields.DateField(attr='created_at')
    updated_at = fields.DateField(attr='updated_at')

    document_id = fields.IntegerField()
    quote = fields.TextField()
    text = fields.TextField()
    tags = fields.ListField(fields.TextField())

    def prepare_document_id(self, instance):
        return instance.document.id

    def prepare_quote(self, instance):
        return instance.quote

    def prepare_text(self, instance):
        return instance.text

    def prepare_tags(self, instance):
        return instance.tags

    class Meta:
        model = Annotation
        ignore_signals = settings.ES_IGNORE_SIGNALS
        auto_refresh = settings.ES_AUTO_REFRESH
