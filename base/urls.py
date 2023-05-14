from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from.views import event_views,order_view,user_view



urlpatterns = [
    path('', user_view.index),
    # signin
    path('login/', user_view.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path("token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
    # signup
    path("register/", user_view.register , name="register"),
    #logout
    path("logout/", user_view.do_logout, name="logout"),
    # users-info
    path('addinfo/', user_view.UserInformationView.as_view()),
    path("addinfo/<int:id>", user_view.UserInformationView.as_view(), name="userinfo_id"),
    # events
    path("events/",event_views.events, name="show_all_events"),
    path("events/<int:pk>",event_views.events, name="show_one_event"),
    # orders
    path('add-to-cart/', order_view.OrderViewSet.as_view({'post': 'add_to_cart'})),
    path('view-cart/', order_view.OrderViewSet.as_view({'get': 'view_cart'})),
    path('update-order/<int:pk>', order_view.OrderViewSet.as_view({'put': 'update_order'})),
    path('remove-from-cart/<int:pk>', order_view.OrderViewSet.as_view({'delete': 'remove_from_cart'})),
    path('place-order/', order_view.OrderViewSet.as_view({'post': 'place_order'})),
    path("purchases/", order_view.UserPurchasesView.as_view(), name="name='user_purchases'"),
    #admin zone:
    path("images/", event_views.EventImageViewSet.as_view({'get': 'list', 'post': 'create'}), name="event_images"),
    path("images/<int:pk>", event_views.EventImageViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name="event_image_detail"),
    path("manage_events/", event_views.EventViewSet.as_view({'get': 'list','post': 'create'}), name="changing_events_by_id"),
    path("manage_events/<int:pk>", event_views.EventViewSet.as_view({'get': 'retrieve','delete': 'destroy', 'put': 'update'}), name="changing_events_by_id"),
    path("all_users/", user_view.get_users),
    path("allpurchases/", order_view.AdminPurchaseListView.as_view(), name="admin-purchases-list")



]