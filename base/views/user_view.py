# Rest Framework Import #
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

# Django Import #
from django.contrib.auth import logout
from django.contrib.auth.models import User
import logging

# Local Import #
from ..serializer import UserInformationSerializer, UserSerializer
from ..models import UserInformation

logger = logging.getLogger('main')

@api_view(['GET'])
def index(req):
    return Response("hello")

#### login ####
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims
        token['username'] = user.username
        if user.is_staff:
            token['is_admin'] = True
        logger.info('User logged success')
        return token
 
####  signin/Login
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

###### register ######
@api_view(['POST'])
def register(req):
    username = req.data["username"]
    password = req.data["password"]
    # create a new user (encrypt password)
    try:
        User.objects.create_user(username=username, password=password)
    except:
        logger.info('User Registered failed')
        return Response("User Registered failed", status=status.HTTP_400_BAD_REQUEST)
    logger.info('User Registered success')
    return Response(f"{username} registered")



####### Log Out #########
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def do_logout(request):
    logout(request)
    logger.info('User Logout success')
    return Response({"detail":"logout"}, status=status.HTTP_202_ACCEPTED)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def get_users(request):
    """
    List of all users.
    """
    users = User.objects.all()
    serializer = UserSerializer(users, many = True)
    return Response(serializer.data)



####### full CRUD for user's information #########

@permission_classes([IsAuthenticated])
class UserInformationView(APIView):
    """
    This class handle the CRUD operations for UserInformation
    """
    def get(self, request):
        """
        Handle GET requests to return a list of USER model
        """
        user=request.user
        my_model = user.userinformation_set.all()
        serializer = UserInformationSerializer(my_model, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def post(self, request):
        """
        Handle POST requests to create a new UserInformation object
        """
        # usr =request.user
        # print(usr)
        serializer = UserInformationSerializer(data=request.data, context={'user': request.user})
        if serializer.is_valid():
            serializer.save()
            logger.info('User Info Created success')
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        logger.info('User Info failed to create')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
   
    def put(self, request, id):
        """
        Handle PUT requests to update an existing UserInformation object
        """
        user=request.user
        my_model = user.userinformation_set.all().first()
        serializer = UserInformationSerializer(my_model, data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info('User Info updated successfly')
            return Response(serializer.data)
        logger.info('User Info update faild')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
   
    def delete(self, request, id):
        """
        Handle DELETE requests to delete a UserInformation object
        """

        my_model = UserInformation.objects.get(pk=id)
        my_model.delete()
        logger.info('User Info deleted successfly')
        return Response(status=status.HTTP_204_NO_CONTENT)

#####################*END CRUD ##################   