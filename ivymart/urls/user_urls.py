from django.urls import path
from ivymart.views.user_views import RegisterUserCreatView, getUserProfile, updateUserProfile, getUsers, getUserById, updateUser, deleteUser
from ivymart.views.jwt_views import MyTokenObtainPairView


urlpatterns = [
    path('register_user/',RegisterUserCreatView.as_view(),name='register_user'),
    path('login/', MyTokenObtainPairView.as_view(), name='login'),
    path('user/list/',getUsers,name="list_users"),
    path('user_profile/', getUserProfile,name="user_profile"),
    path('profile/update/',updateUserProfile,name="user_profile_update"),
    path('user/<str:pk>/',getUserById,name="get_user"),
    path('update_user/<str:pk>/',updateUser,name="update_user"),
    path('delete_user/<str:pk>/',deleteUser,name="delete_user"),
]