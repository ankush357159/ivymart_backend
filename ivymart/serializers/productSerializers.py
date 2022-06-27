from rest_framework import serializers
from ivymart.models import Review, Product, ShippingAddress
from django.conf import settings

import cloudinary
import cloudinary.uploader


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    reviews = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Product
        fields = "__all__"

    def get_reviews(self, obj):
        reviews = obj.review_set.all()
        serializer = ReviewSerializer(reviews, many=True)
        return serializer.data

    


class ShippingAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingAddress
        fields = "__all__"


class NewProductSerializer(serializers.ModelSerializer):
    image = serializers.ImageField()

    class Meta:
        model = Product
        fields = [
            "id",
            "user",
            "name",
            "image",
            "brand",
            "category",
            "description",
            "rating",
            "numReviews",
            "price",
            "countInStock",
            "createdAt",
        ]

    def create(self, validated_data):
        user = validated_data.get("user")
        name = validated_data.get("name")
        image = validated_data.pop("image")
        brand = validated_data.get("brand")
        category = validated_data.get("category")
        description = validated_data.get("description")
        rating = validated_data.get("rating")
        numReviews = validated_data.get("numReviews")
        price = validated_data.get("price")
        countInStock = validated_data.get("countInStock")

        product = Product(**validated_data)
        product.save()
        try:
            image_data = cloudinary.uploader.upload(
                image,
                public_id="myapp/myimages/",
                crop="fill",
                width="500",
                height="500",
            )
            product.is_deleted = False
            product.save()

        except:
            product.delete()
            raise serializers.ValidationError({"images": "cloudinary failed to upload"})
        return product
