from django.urls import path
from ivymart.views.product_views import (
    NewProductView,
    getProducts,
    createProductReview,
    getProduct,
    getTopProducts,
    updateImage,
    updateProduct,
    deleteProduct,
    uploadImage,
    CreateProductView,
    ProductUpdateView,
    createProduct,
    getProductList,
    querybyCategory,
)


urlpatterns = [
    path("create_product/", CreateProductView.as_view(), name="new_product"),
    path("product/create/", createProduct, name="product_create"),
    path("product/new/", NewProductView.as_view(), name="product_new"),
    path("upload/image/", uploadImage, name="upload_image"),
    path("update_image/", updateImage, name="upload_image"),
    path("list_products/", getProducts, name="list_products"),
    path("list/all/products/", getProductList, name="list_all_products"),
    path("product_details/<str:pk>/", getProduct, name="product_details"),
    path("create/review/<str:pk>/", createProductReview, name="create_review"),
    path("top_products/", getTopProducts, name="top_products"),
    path("update_product/<str:pk>/", updateProduct, name="update_product"),
    path("delete_product/<str:pk>/", deleteProduct, name="delete_product"),   
    path("search/product/", querybyCategory, name="search_products"),   
]


