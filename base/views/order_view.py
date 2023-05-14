# Rest Framework Import #
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.views import APIView

# Local Import #
from ..models import Event, Order, Purchase
from ..serializer import OrderSerializer, PurchaseSerializer
import logging

logger = logging.getLogger('main')

class OrderViewSet(viewsets.ModelViewSet):
    """
    OrderViewSet handles all the operations related to orders:
    add, view, update, and delete.

    Only authenticated users are allowed to access the endpoint.
    """
    permission_classes = [IsAuthenticated]
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    @action(detail=False, methods=['post'])
    def add_to_cart(self, request):
        pk=request.data['pk']
        quantity=request.data['quantity']
        """
        Adds the tickets to the cart.

        The number of tickets in the cart can't be more than the quantity available in the event.
        """ 
        if pk==None:
            return Response({'message': 'event_id is required!'}, status=400)
        event = Event.objects.get(id=pk)
        if quantity > event.quantity:
            return Response({'message': 'Not enough tickets available!'}, status=400)
        subtotal = event.price * quantity
        order = Order.objects.create(
            user=request.user,
            event=event,
            quantity=quantity,
            subtotal=subtotal
        )
        logger.info('User added tickets successfully')
        return Response({'message': 'Tickets added to cart successfully!'},status=202)

    @action(detail=False, methods=['get'])
    def view_cart(self, request):
        """
        Views the current cart.
        """
        orders = Order.objects.filter(user=request.user)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['put'])
    def update_order(self, request, pk):
        """
        Updates the number of tickets in the cart.
        """
        order = Order.objects.get(id=pk)
        quantity = request.data['quantity']
        if int(quantity) > order.event.quantity:
            logger.info('User update tickets faild')
            return Response({'message': 'Not enough tickets available!'}, status=400)
        order.quantity = int(quantity)
        order.subtotal = order.event.price * order.quantity
        order.save()
        logger.info('User update tickets successfully')
        return Response({'message': 'Order updated successfully!'},status=200)

    @action(detail=True, methods=['delete'])
    def remove_from_cart(self, request, pk):
        """
        Removes the tickets from the cart.
        """
        Order.objects.get(id=pk).delete()
        logger.info('User remove tickets successfully')
        return Response({'message': 'Order removed from cart successfully!'},status=200)

    @action(detail=True, methods=['post'])
    def place_order(self, request,pk=None):
        """
        Place the order and update the Purchase model with the order information.
        """
        user = request.user
        order_items = Order.objects.filter(user=user)
        if not order_items:
            return Response({'message': 'Your cart is empty!'}, status=400)
    
        total = sum([item.subtotal for item in order_items])
        Purchase.objects.bulk_create([
            Purchase(
                user=user,
                event=item.event,
                quantity=item.quantity,
                subtotal=item.subtotal,
             ) for item in order_items
    ])
        for item in order_items:
         # Update the quantity of the event
            event = item.event
            print(item.quantity)
            event.quantity -= item.quantity
            event.save()

        order_items.delete()
        logger.info('User order placed successfully')
        return Response({'message': 'Order placed successfully!'})



class UserPurchasesView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        """
        View all the purchase have been made by specific user
        """
        purchases = Purchase.objects.filter(user=request.user)
        serializer = PurchaseSerializer(purchases, many=True)
        return Response(serializer.data)
    
    
class AdminPurchaseListView(APIView):
    permission_classes = [IsAdminUser]
    def get(self, request):
        """
        Views all the purchase that have been made by all users - only for admin!
        """
        purchases = Purchase.objects.all().order_by('-date')
        serializer = PurchaseSerializer(purchases, many=True)
        return Response(serializer.data)

    
    
    
    
