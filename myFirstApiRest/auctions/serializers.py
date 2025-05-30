from rest_framework import serializers
from django.utils import timezone
from .models import Category, Auction, Bid, Rating, Comment
from drf_spectacular.utils import extend_schema_field

class CategoryListCreateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Category
        fields = ['id','name']

class CategoryDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = "__all__"

class AuctionListCreateSerializer(serializers.ModelSerializer):
    creation_date = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%SZ", read_only=True)
    closing_date = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%SZ")
    isOpen = serializers.SerializerMethodField(read_only=True)
    average_rating = serializers.FloatField(read_only=True)
    thumbnail_url = serializers.SerializerMethodField()  # Campo adicional para la URL de la imagen

    class Meta:
        model = Auction
        fields = "__all__"

    @extend_schema_field(serializers.BooleanField())
    def get_isOpen(self, obj):
        return obj.closing_date > timezone.now()

    def get_thumbnail_url(self, obj):
        request = self.context.get('request')  # Esto es necesario para generar la URL absoluta
        if obj.thumbnail and request:
            return request.build_absolute_uri(obj.thumbnail.url)  # Devuelve la URL completa
        return None

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("El precio debe ser mayor que cero.")
        return value
    
    def validate_stock(self, value):
        if value <= 0:
            raise serializers.ValidationError("El stock debe ser mayor que cero.")
        return value
    
    def validate_rating(self, value):
        if value < 0 or value > 5:
            raise serializers.ValidationError("La calificación debe estar entre 0 y 5.")
        return value
    
    def validate(self, data):
        creation_date = self.instance.creation_date if self.instance else timezone.now()
        closing_date = data.get("closing_date", getattr(self.instance, "closing_date", None))

        if closing_date is None:
            raise serializers.ValidationError("Se requiere una fecha de cierre válida.")

        if closing_date <= creation_date:
            raise serializers.ValidationError("La fecha de cierre debe ser posterior a la de creación.")
        
        if closing_date <= creation_date + timezone.timedelta(days=15):
            raise serializers.ValidationError("La subasta debe durar al menos 15 días.")
        
        return data



class AuctionDetailSerializer(serializers.ModelSerializer):
    creation_date = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%SZ", read_only=True)
    closing_date = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%SZ")
    isOpen = serializers.SerializerMethodField(read_only=True)
    average_rating = serializers.FloatField(read_only=True)
    thumbnail_url = serializers.SerializerMethodField()  # Campo adicional para la URL de la imagen

    class Meta:
        model = Auction
        fields = "__all__"
    
    @extend_schema_field(serializers.BooleanField())
    def get_isOpen(self, obj):
        return obj.closing_date > timezone.now()

    def get_thumbnail_url(self, obj):
        # Retorna la URL completa de la imagen
        return obj.thumbnail.url if obj.thumbnail else None

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("El precio debe ser mayor que cero.")
        return value
    
    def validate_stock(self, value):
        if value <= 0:
            raise serializers.ValidationError("El stock debe ser mayor que cero.")
        return value
    
    def validate(self, data):
        creation_date = self.instance.creation_date if self.instance else timezone.now()
        closing_date = data.get("closing_date", getattr(self.instance, "closing_date", None))

        if closing_date is None:
            raise serializers.ValidationError("Se requiere una fecha de cierre válida.")

        if closing_date <= creation_date:
            raise serializers.ValidationError("La fecha de cierre debe ser posterior a la de creación.")
        
        if closing_date <= creation_date + timezone.timedelta(days=15):
            raise serializers.ValidationError("La subasta debe durar al menos 15 días.")
        
        return data



class BidListCreateSerializer(serializers.ModelSerializer):
    creation_date = serializers.DateTimeField(read_only=True, format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = Bid
        fields = "__all__"

class BidDetailSerializer(serializers.ModelSerializer):
    creation_date = serializers.DateTimeField(read_only=True, format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = Bid
        fields = "__all__"

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['id', 'points']  # Solo estos, porque los otros los añades en la view

    def create(self, validated_data):
        auction_id = self.context['view'].kwargs['auction_id']
        reviewer = self.context['request'].user

        rating, _ = Rating.objects.update_or_create(
            reviewer=reviewer,
            auction_id=auction_id,
            defaults={'points': validated_data['points']}
        )
        return rating

class CommentSerializer(serializers.ModelSerializer):
    reviewer_username = serializers.ReadOnlyField(source='reviewer.username')

    class Meta:
        model = Comment
        fields = ['id', 'title', 'content', 'created_at', 'updated_at', 'reviewer', 'reviewer_username', 'auction']
        read_only_fields = ['reviewer', 'created_at', 'updated_at', 'auction']
