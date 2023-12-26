from django.urls import path
from .views import (ViewProfile, ViewAllCustomerProfiles, CreateCompleteProfile,
                    UpdateProfile)


urlpatterns = [
    path('update_profile', UpdateProfile.as_view(), name='update-profile'),
    path('complete_profile', CreateCompleteProfile.as_view(), name='complete_profile'),
    path('me', ViewProfile.as_view(), name='view-my-profile'),
    path('view_all', ViewAllCustomerProfiles.as_view(), name='view_all'),

]
