from django.views.generic import ListView, DetailView
from crime.models import Crime

from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Sum
from crime.serializers import CrimeSerializer


class CrimeViewSet(viewsets.ModelViewSet):
    """
    API endpoint for viewing and editing crimes.
    """
    queryset = Crime.objects.all().order_by('-created_at')
    serializer_class = CrimeSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'count', 'created_at', 'updated_at']

    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """
        Custom endpoint to get crime statistics
        """
        total_crimes = Crime.objects.aggregate(
            total_count=Sum('count'),
            total_records=Count('id')
        )
        return Response(total_crimes)

    @action(detail=True, methods=['get'])
    def timeline(self, request, pk=None):
        """
        Get the timeline of a specific crime
        """
        crime = self.get_object()
        return Response({
            'created_at': crime.created_at,
            'updated_at': crime.updated_at,
        })


class CrimeListView(ListView):
    model = Crime
    template_name = 'crimes/crime_list.html'
    context_object_name = 'crimes'
    ordering = ['-created_at']
    paginate_by = 10  # Optional: adds pagination every 10 items


class CrimeDetailView(DetailView):
    model = Crime
    template_name = 'crimes/crime_detail.html'
    context_object_name = 'crime'
