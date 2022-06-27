# Django Import
from lib2to3.pgen2.parse import ParseError
from unicodedata import category
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import re
from django.db.models import Q

# import cloudinary
# import cloudinary.uploader
from django.http import JsonResponse
from django.shortcuts import get_object_or_404


# Rest Framework Import
from rest_framework import status, viewsets
from rest_framework.decorators import api_view, permission_classes, APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.parsers import (
    MultiPartParser,
    FormParser,
    JSONParser,
    FileUploadParser,
)


# Local Import
from ivymart.models import Product, Review
from ivymart.serializers.productSerializers import (
    ProductSerializer,
    NewProductSerializer,
)


# Create Product - Admin
class CreateProductView(generics.CreateAPIView):
    queryset = Product.objects.all()
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    serializer_class = ProductSerializer


# Create a new Product -- Admin
@api_view(["POST"])
@permission_classes([IsAdminUser])
def createProduct(request, *args, **kwargs):
    product = Product.objects.create(
        user=request.user,
        name=request.data["name"],
        brand=request.data["brand"],
        category=request.data["category"],
        price=request.data["price"],
        description=request.data["description"],
        countInStock=request.data["countInStock"],
        image=request.data["image"],
    )
    product.save()
    serializer = ProductSerializer(product, many=False)
    return Response(serializer.data)


# Upload Image -- Admin
@api_view(["POST"])
@permission_classes([AllowAny])
def uploadImage(request):
    try:
        image = request.data["image", "Default"]
    except KeyError:
        raise ParseError("Request has no resource file attached")
    file = request.data
    image = Product.objects.create(image=file)
    image.save()
    return Response("Image was uploaded")


# Update Image -- Admin
@api_view(["PUT"])
@permission_classes([AllowAny])
def updateImage(request):
    data = request.data
    product_id = data["product_id"]
    product = Product.objects.get(id=product_id)
    product.image = request.FILES.get("image")
    product.save()
    return Response("Image was uploaded")


# Get all the products
@api_view(["GET"])
def getProductList(request):

    products = Product.objects.all().order_by("-id")
    page = request.GET.get("page", 1)

    paginator = Paginator(products, 5)

    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)


# Get all the products with query
@api_view(["GET"])
def getProducts(request):
    query = request.query_params.get("keyword")
    print(query)
    if query == None:
        query = ""

    products = Product.objects.filter(description__icontains=query).order_by("-id")

    page = request.query_params.get("page")
    paginator = Paginator(products, 5)

    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    if page == None:
        page = 1
    # page = int(page.replace("/", "").strip())
    page = int(page)

    serializer = ProductSerializer(products, many=True)
    return Response(
        {"products": serializer.data, "page": page, "pages": paginator.num_pages}
    )


# Top Products
@api_view(["GET"])
def getTopProducts(request):
    products = Product.objects.filter(rating__gte=4).order_by("-rating")[0:5]
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)


# Get a Product
@api_view(["GET"])
def getProduct(request, pk):
    product = Product.objects.get(id=pk)
    serializer = ProductSerializer(product, many=False)
    return Response(serializer.data)


# Update a Product
@api_view(["PUT"])
@permission_classes([IsAdminUser])
def updateProduct(request, pk):
    data = request.data
    product = Product.objects.get(id=pk)

    product.name = data["name"]
    product.price = data["price"]
    product.brand = data["brand"]
    product.countInStock = data["countInStock"]
    product.category = data["category"]
    product.description = data["description"]

    product.save()

    serializer = ProductSerializer(product, many=False)
    return Response(serializer.data)


# Delete a Product
@api_view(["DELETE"])
@permission_classes([IsAdminUser])
def deleteProduct(request, pk):
    product = Product.objects.get(id=pk)
    product.delete()
    return Response("Product deleted successfully")


# Create Product Review
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def createProductReview(request, pk):
    user = request.user
    product = Product.objects.get(id=pk)
    data = request.data

    # 1 Review already exists
    alreadyExists = product.review_set.filter(user=user).exists()

    if alreadyExists:
        content = {"detail": "Product already reviewed by you"}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)

    # 2 No Rating or 0
    elif data["rating"] == 0:
        content = {"detail": "Please Select a rating"}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)

    # 3 Create review
    else:
        review = Review.objects.create(
            user=user,
            product=product,
            name=user.username,
            rating=data["rating"],
            comment=data["comment"],
            heading=data["heading"],
        )

        reviews = product.review_set.all()
        product.numReviews = len(reviews)

        total = 0

        for i in reviews:
            total += i.rating
        product.rating = total / len(reviews)
        product.save()

        return Response("Review Added")


class ProductView(APIView):
    permission_classes = [AllowAny]

    def list(self, request):
        product = Product.objects.all()
        product_serializer = ProductSerializer(product, many=True)
        return Response(product_serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        product_serializer = ProductSerializer(data=request.data)
        product_serializer.is_valid(raise_exception=True)
        product_serializer.save()

    def retrieve(self, request, pk=None):
        product = get_object_or_404(Product, id=pk)
        product_serializer = ProductSerializer(product)
        return Response(product_serializer.data, status=status.HTTP_200_OK)

    def update(self,request,pk=None,):
        product = get_object_or_404(Product, id=pk)
        product_serializer = ProductSerializer(instance=product, data=request.data)
        product_serializer.is_valid(raise_exception=True)
        product_serializer.save()
        return Response(product_serializer.data, status=status.HTTP_200_OK)

    def delete(self,request,pk=None,):
        product = get_object_or_404(Product, id=pk)
        product.delete()
        return Response({"msg": "Product deleted"}, status=status.HTTP_204_NO_CONTENT)


class ProductCreateView(generics.CreateAPIView):
    queryset = Product.objects.all()
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    serializer_class = ProductSerializer


class ProductUpdateView(generics.UpdateAPIView):
    queryset = Product.objects.all()
    permission_classes = [IsAuthenticated]
    parser_classes = [FormParser, JSONParser, FileUploadParser]
    serializer_class = ProductSerializer


class NewProductView(APIView):
    parser_classes = [
        MultiPartParser,
    ]

    def post(self, request, format=None):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

# Querying views : category - appliances
@api_view(["GET"])
def querybyCategory(request):
    query = request.query_params.get("keyword")
    print(query)
    if query == None:
        query = ""
    products = Product.objects.filter(Q(category=query)).order_by("-id")
    # Q(category="query") & Q(name__icontains="silk")
    page = request.query_params.get("page")
    page = request.GET.get("page", 1)
    paginator = Paginator(products, 5)

    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    serializer = ProductSerializer(products, many=True)
    return Response(
    {"products": serializer.data, "page": page, "pages": paginator.num_pages}
    )


# #Upload image in cloudinary
# # Upload Image -- Admin
# @api_view(["PUT"])
# @permission_classes([AllowAny])
# def uploadImage(request):
#     product = Product.objects.all()
#     product.image = request.FILES["image"]
#     try:
#         cloudinary.uploader.upload(request.FILES["image"])
#         return Response("Image uploaded successfully")
#     except:
#         return Response("Image could not be uploaded")


# Delete a Product with cloudinary
# @api_view(["DELETE"])
# @permission_classes([IsAdminUser])
# def deleteProduct(request, pk):
#     product = Product.objects.get(id=pk)
#     cloudinary.uploader.destroy(product.image.public_id, invalidate=True)
#     product.delete()
#     return Response("Product deleted successfully")
