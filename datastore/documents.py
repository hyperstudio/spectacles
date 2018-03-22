from django_elasticsearch_dsl import DocType, Index, fields
from spectacles.utils import DictModel
from datastore.models import Annotation
from datastore.models import Document
from django.conf import settings

class ESModel(DictModel):
    _json_fields = []

    def to_dict(self, **kwargs):
        data = DocType.to_dict(self)
        meta = self.meta.to_dict()
        data.update(meta)
        return data

# TODO: add archive_id to both annotation and document


document_index = Index('spectacles-document')
document_index.settings(
    number_of_shards=1,
    number_of_replicas=0
)
@document_index.doc_type
class ESDocument(ESModel, DocType):
    id = fields.IntegerField(attr='id')
    # TODO: add user id to creator field
    creator = fields.ObjectField(properties={
        'email': fields.TextField(),
        'name': fields.TextField(),
    })
    text = fields.TextField(attr='text')
    title = fields.TextField(attr='title')
    author = fields.TextField(attr='author')
    created_at = fields.DateField(attr='created_at', default_timezone='UTC')
    updated_at = fields.DateField(attr='updated_at', default_timezone='UTC')

    def get_queryset(self):
        return super(ESDocument, self).get_queryset().order_by('id')

    class Meta:
        model = Document
        ignore_signals = settings.ES_IGNORE_SIGNALS
        auto_refresh = settings.ES_AUTO_REFRESH
        queryset_pagination = 200



annotation_index = Index('spectacles-annotation')
annotation_index.settings(
    number_of_shards=1,
    number_of_replicas=0
)
@annotation_index.doc_type
class ESAnnotation(ESModel, DocType):
    id = fields.IntegerField(attr='id')
    uuid = fields.TextField(attr='uuid')
    creator = fields.ObjectField(properties={
        'email': fields.TextField(),
        'name': fields.TextField(),
    })
    created_at = fields.DateField(attr='created_at', default_timezone='UTC')
    updated_at = fields.DateField(attr='updated_at', default_timezone='UTC')

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

    def get_queryset(self):
        return super(ESAnnotation, self).get_queryset().order_by('id')

    class Meta:
        model = Annotation
        ignore_signals = settings.ES_IGNORE_SIGNALS
        auto_refresh = settings.ES_AUTO_REFRESH
        queryset_pagination = 500
