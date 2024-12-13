from pyexpat.errors import messages
from rest_framework import viewsets, filters
from rest_framework.decorators import action
from wamex.serializers import SpatialMetaDataSerializer
from wamex.models import SpatialMetaData, Chat
# decorator csrf_exempt
from django.views.decorators.csrf import csrf_exempt
from wamex.utils import QdrantSearch, logger
from rest_framework.response import Response
# import AllowAny
from rest_framework.permissions import AllowAny
from fastembed import TextEmbedding


class SpatialMetaDataViewSet(viewsets.ModelViewSet):
    queryset = SpatialMetaData.objects.all().order_by('-created_at')
    serializer_class = SpatialMetaDataSerializer
    permission_classes = [AllowAny]  # Add

    @csrf_exempt
    @action(detail=False, methods=['post'], url_path='chat')
    def chat(self, request):
        """
        Custom endpoint to get chat
        """
        chat_uuid = request.data.get('chat_uuid', None)
        if not chat_uuid:
            return Response(
                {'error': 'chat_uuid is required'}
            )
        chat = Chat.objects.filter(uuid=chat_uuid).first()
        if not chat:
            return Response(
                {'error': 'Chat not found'}
            )
        messages = chat.messages["messages"]
        question = request.data.get('question', None)

        # embed the question with fastembed
        embedding = TextEmbedding()
        question_embedding = embedding.embed([question])
        question_embedding = list(question_embedding)[0].tolist()
        # we want to do the search on qdrant
        qdrant_search = QdrantSearch(collection_name='wamex')
        # search for the question in qdrant
        response = qdrant_search.search_metadata(question_embedding)
        # construct a related files list
        first_result = None
        for res in response:
            if first_result is None:
                first_result = res
            messages.append({
                "role": "bot",
                "content": res["payload"]["file_name"]
            })
        chat.messages["messages"] = messages
        chat.save()

        spatial_data = SpatialMetaData.objects.filter(file_name=first_result["payload"]["file_name"]).first()
        if not spatial_data:
            return Response(
                {'error': 'Spatial Data not found'}
            )

        # we want to return the geometry to the user
        return Response(
            {'geometry': spatial_data.geometry.geojson}
        )
