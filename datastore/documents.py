from django_elasticsearch_dsl import DocType, Index, fields
from app.utils import DictModel
from datastore.models import Annotation
from datastore.models import Document
from django.conf import settings

class ESModel(DictModel):
    _json_fields = []

    def to_dict(self):
        data = DocType.to_dict(self)
        meta = self.meta.to_dict()
        data['_meta'] = meta
        return data

document_index = Index('spectacles-document')
document_index.settings(
    number_of_shards=1,
    number_of_replicas=0
)
@document_index.doc_type
class ESDocument(DocType, ESModel):
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
class ESAnnotation(DocType, ESModel):
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

    def to_dict(self):
        data = DocType.to_dict(self)
        meta = self.meta.to_dict()
        data['_meta'] = meta
        return data
