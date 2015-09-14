# -*- coding: utf-8 -*-
from rest_framework import serializers, viewsets
from project.core.models import Purchase, Product, Catalog, ProductImages, Promo, CatalogProductProperties, PurchaseStatusLinks, PurchaseStatus, Category, PurchaseQuestion, PurchaseAnswer
from project.accounts.models import OrganizerProfile
from project.documentation.models import Page
from django.contrib.auth.models import User


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImages
        fields = ('image', 'cropping', 'cropping_url', 'cropping_url_cart', 'p_image_title')


class ProductSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ('id', 'sku', 'product_name', 'description', 'price', 'property', 'images', 'catalog')


class CatalogPropertiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = CatalogProductProperties
        fields = ('id', 'cpp_name', 'cpp_slug', 'cpp_values')


class CatalogSerializer(serializers.ModelSerializer):
    product_catalog = ProductSerializer(many=True, read_only=True)
    cpp_catalog = CatalogPropertiesSerializer(many=True, read_only=True)

    class Meta:
        model = Catalog
        fields = ('id', 'catalog_name', 'cpp_catalog', 'product_catalog')


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseStatus


class PurchaseStatusSerializer(serializers.ModelSerializer):
    status = StatusSerializer()

    class Meta:
        model = PurchaseStatusLinks


class PurchaseSerializer(serializers.ModelSerializer):
    catalogs = CatalogSerializer(many=True, read_only=True)
    purchase_status = PurchaseStatusSerializer(many=True, read_only=True)

    class Meta:
        model = Purchase
        fields = ('id', 'name', 'description', 'purchase_status', 'catalogs')


class OrganizerSerializer(serializers.ModelSerializer):
    purchases = PurchaseSerializer(many=True, read_only=True)

    class Meta:
        model = OrganizerProfile
        fields = ('icon', 'purchases')


class PromoSerializer(serializers.ModelSerializer):
    promo_purchase = PurchaseSerializer(many=True, read_only=True)

    class Meta:
        model = Promo
        fields = ('name', 'alias', 'promo_purchase')


class CategorySerializer(serializers.ModelSerializer):
    category_purchase = PurchaseSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ('id', 'name', 'slug', 'parent', 'category_purchase')


class BenefitsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = ('id', 'name', 'description')


class AnswersSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseAnswer
        fields = ('id', 'user', 'text', 'question' )


class QuestionsSerializer(serializers.ModelSerializer):
    answers = AnswersSerializer(many=True, read_only=True)
    class Meta:
        model = PurchaseQuestion
        fields = ('id', 'user', 'text', 'purchase', 'product', 'answers' )


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')
