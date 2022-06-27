from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/products/", include("ivymart.urls.product_urls")),
    path("api/v1/users/", include("ivymart.urls.user_urls")),
    path("api/v1/orders/", include("ivymart.urls.order_urls")),
    path("api/v1/stripe/", include("ivymart.urls.stripe_urls")),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
