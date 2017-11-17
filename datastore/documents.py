from django_elasticsearch_dsl import DocType, Index, fields
from datastore.models import Annotation
from datastore.models import Document


document_index = Index('spectacles-document')
document_index.settings(
    number_of_shards=1,
    number_of_replicas=0
)
@document_index.doc_type
class ESDocument(DocType):
    creator = fields.ObjectField(properties={
        'email': fields.TextField(),
        'name': fields.TextField(),
    })
    id = fields.IntegerField(attr='id')
    text = fields.TextField(attr='text')
    title = fields.TextField(attr='title')
    author = fields.TextField(attr='author')
    created_at = fields.DateField(attr='created_at')
    updated_at = fields.DateField(attr='updated_at')
    annotations = fields.NestedField(properties={
        'uuid': fields.TextField(),
        'quote': fields.TextField(),
        'text': fields.TextField(),
        'tags': fields.ListField(fields.TextField()),
        'creator': fields.ObjectField(properties={
            'email': fields.TextField(),
            'name': fields.TextField(),
        }),
    })

    class Meta:
        model = Document
        related_models = [Annotation]

    def get_queryset(self):
        return super(ESDocument, self).get_queryset()

    def get_instances_from_related(self, related_instance):
        return related_instance.document


annotation_index = Index('spectacles-annotation')
annotation_index.settings(
    number_of_shards=1,
    number_of_replicas=0
)
@annotation_index.doc_type
class ESAnnotation(DocType):
    quote = fields.TextField()
    text = fields.TextField()
    tags = fields.ListField(fields.TextField())
    creator = fields.ObjectField(properties={
        'email': fields.TextField(),
        'name': fields.TextField(),
    })
    created_at = fields.DateField(attr='created_at')
    updated_at = fields.DateField(attr='updated_at')

    def prepare_quote(self, instance):
        return instance.quote

    def prepare_text(self, instance):
        return instance.text

    def prepare_tags(self, instance):
        return instance.tags

    class Meta:
        model = Annotation
