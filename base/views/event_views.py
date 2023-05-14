# Rest Framework Import #
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status, viewsets

# Django Import #
from django.shortcuts import get_object_or_404
import datetime 
import logging

# Local Import #
from ..models import Event, EventImage
from ..serializer import EventSerializer, ImageSerializer

logger = logging.getLogger('main')

##### Get all the list of events #####
@permission_classes([AllowAny])
@api_view(['GET'])
def events(req,pk=None):
    """
    List of all events
    """
    if pk != None:
        try:
            event = Event.objects.get(pk=pk)
        except Event.DoesNotExist:
            return Response({'error': 'Event with id {} does not exist'.format(pk)}, status=status.HTTP_404_NOT_FOUND)
        serializer = EventSerializer(event)
        return Response(serializer.data)
    today = datetime.datetime.now()
    all_events = Event.objects.filter(date_and_time__gte=today).order_by('date_and_time')
    serializer = EventSerializer(all_events, many=True)
    return Response(serializer.data)


######### Complete CRUD for Event table ##############


class EventViewSet(viewsets.ModelViewSet):
    """
    This class handle the CRUD operations for Event
    """
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    parser_classes = [MultiPartParser, FormParser]
    
    @permission_classes([AllowAny])
    def retrieve(self, request, pk=None):
        """
        Handle GET request to return a list or one object of Event table
        """
        try:
            event = Event.objects.get(pk=pk)
        except Event.DoesNotExist:
            return Response({'error': 'Event with id {} does not exist'.format(pk)}, status=status.HTTP_404_NOT_FOUND)
        serializer = EventSerializer(event)
        return Response(serializer.data)

    @permission_classes([IsAdminUser])
    def create(self, request):
        """
        Handle POST requests to create a new Event object
        """
        event_serializer = EventSerializer(data=request.data)
        if event_serializer.is_valid():
            event = event_serializer.save()
            event_image = request.FILES.get('image')
            if event_image:
                event_image_serializer = ImageSerializer(data={'image': event_image, 'title': event.event_name})
                if event_image_serializer.is_valid():
                    event_image = event_image_serializer.save()
                    event.image = event_image
                    event.save()
                else:
                    event.delete()
                    logger.info('Creating new event faild')
                    return Response(event_image_serializer.errors,
                                    status=status.HTTP_400_BAD_REQUEST)
            logger.info('Created new event successfully')                        
            return Response(event_serializer.data, status=status.HTTP_201_CREATED)
        logger.info('Creating new event faild')
        return Response(event_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @permission_classes([IsAdminUser])
    def update(self, request, pk):
        """
        Handle PUT requests to update an existing Event object
        """
        event = self.get_object()
        event_serializer = EventSerializer(event, data=request.data, partial=True)
        if event_serializer.is_valid():
            event = event_serializer.save()
            event_image = request.FILES.get('image')
            if event_image:
                if event.image:
                    event.image.image = event_image
                    event.image.save()
                else:
                    event_image_serializer = ImageSerializer(data={'image': event_image, 'title': event.event_name})
                    if event_image_serializer.is_valid():
                        event_image = event_image_serializer.save()
                        event.image = event_image
                        event.save()
                    else:
                        logger.info('Updated event faild')  
                        return Response(event_image_serializer.errors,
                                        status=status.HTTP_400_BAD_REQUEST)
            logger.info('Updated event successfully')                              
            return Response(event_serializer.data, status=status.HTTP_200_OK)
        logger.info('Updated event faild')  
        return Response(event_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @permission_classes([IsAdminUser])
    def destroy(self, request, pk):
        """
        Handle DELETE requests to delete a Event object
        """
        event = self.get_object()
        event.delete()
        logger.info('Event deleted successfully')  
        return Response(status=status.HTTP_204_NO_CONTENT)

#################### END CRUD #####################



################### Complete CRUD for EventImage #################


class EventImageViewSet(viewsets.ViewSet):
    """
    This class handle the CRUD operations for EventImage
    """
    @permission_classes([AllowAny])
    def list(self, request):
        """
        Handle GET requests to return a list of EventsImage model
        """
        queryset = EventImage.objects.all()
        serializer = ImageSerializer(queryset, many=True)
        return Response(serializer.data)
    
    @permission_classes([AllowAny])
    def retrieve(self, request, pk=None):
        """
        Handle GET requests to return a single object of EventImage model
        """
        queryset = EventImage.objects.all()
        image = get_object_or_404(queryset, pk=pk)
        serializer = ImageSerializer(image)
        return Response(serializer.data)

    @permission_classes([IsAdminUser])
    def create(self, request):
        """
        Handle POST requests to create a new EventImage object
        """
        serializer = ImageSerializer(data=request.data)
        print(request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info('Create new image faild')  
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        logger.info('Create new image successfully')  
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @permission_classes([IsAdminUser])
    def update(self, request, pk=None):
        """
        Handle PUT requests to update EventImage object
        """
        queryset = EventImage.objects.all()
        image = get_object_or_404(queryset, pk=pk)
        serializer = ImageSerializer(image, data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info('Create new image successfully')  
            return Response(serializer.data)
        logger.info('Create new image faild')  
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @permission_classes([IsAdminUser])
    def destroy(self, request, pk=None):
        """
        Handle DELETE requests to delete an existing EventImage object
        """
        queryset = EventImage.objects.all()
        image = get_object_or_404(queryset, pk=pk)
        image.delete()
        logger.info('Image deleted successfully')  
        return Response(status=status.HTTP_204_NO_CONTENT)




#####################*END CRUD ##################