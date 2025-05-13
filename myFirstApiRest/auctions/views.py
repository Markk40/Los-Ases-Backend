from django.shortcuts import render
from django.utils import timezone
# Create your views here.
from rest_framework import generics
from .models import Category, Auction, Bid, Rating, Comment
from .serializers import (
    CategoryListCreateSerializer, CategoryDetailSerializer, 
    AuctionListCreateSerializer, AuctionDetailSerializer, 
    BidListCreateSerializer, BidDetailSerializer, RatingSerializer,
    CommentSerializer
    )
from rest_framework.views import APIView 
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from .permissions import IsOwnerOrAdmin 
from rest_framework.parsers import MultiPartParser, FormParser

class CategoryListCreate(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Category.objects.all()
    serializer_class = CategoryListCreateSerializer

class CategoryRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsOwnerOrAdmin]
    queryset = Category.objects.all()
    serializer_class = CategoryDetailSerializer

class AuctionListCreate(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    serializer_class = AuctionListCreateSerializer
    parser_classes = [MultiPartParser, FormParser]  # Permite el manejo de archivos (imágenes)
    def get_queryset(self):
        queryset = Auction.objects.all()

        # Filtro por valoración mínima
        min_rating = self.request.query_params.get('min_rating')
        if min_rating is not None:
            try:
                min_rating = float(min_rating)
                queryset = queryset.filter(average_rating__gte=min_rating)
            except ValueError:
                pass

        # Filtro por subastas abiertas usando closing_date
        is_open = self.request.query_params.get('is_open')
        if is_open and is_open.lower() == 'true':
            queryset = queryset.filter(closing_date__gt=timezone.now())

        return queryset
    
class AuctionRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsOwnerOrAdmin]
    queryset = Auction.objects.all()
    serializer_class = AuctionDetailSerializer
    parser_classes = [MultiPartParser, FormParser]  # Permite el manejo de archivos (imágenes)

class UserAuctionListView(APIView): 
    permission_classes = [IsAuthenticated] 
    def get(self, request, *args, **kwargs): 
        # Obtener las subastas del usuario autenticado 
        user_auctions = Auction.objects.filter(auctioneer=request.user) 
        serializer = AuctionListCreateSerializer(user_auctions, many=True) 
        return Response(serializer.data)

class BidListCreate(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = BidListCreateSerializer

    def get_queryset(self):
        return Bid.objects.filter(auction_id=self.kwargs['auction_id'])

    def perform_create(self, serializer):
        serializer.save(auction_id=self.kwargs['auction_id'])

class BidRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BidDetailSerializer

    def get_queryset(self):
        return Bid.objects.filter(auction_id=self.kwargs['auction_id'])
    
class RatingListCreate(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RatingSerializer

    def get_queryset(self):
        return Rating.objects.filter(auction_id=self.kwargs['auction_id'], reviewer=self.request.user)

    def perform_create(self, serializer):
        auction_id = self.kwargs['auction_id']
        serializer.save(reviewer=self.request.user, auction_id=auction_id)


class RatingRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsOwnerOrAdmin]  # Solo el dueño o el admin puede editar/eliminar
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer

class MyRatingView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, auction_id, *args, **kwargs):
        try:
            rating = Rating.objects.get(auction_id=auction_id, reviewer=request.user)
            serializer = RatingSerializer(rating)
            return Response(serializer.data)
        except Rating.DoesNotExist:
            return Response({"detail": "Valoración no encontrada"}, status=404)

class CommentListCreate(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = CommentSerializer

    def get_queryset(self):
        return Comment.objects.filter(auction_id=self.kwargs['auction_id'])

    def perform_create(self, serializer):
        auction_id = self.kwargs.get('auction_id')
        serializer.save(
            reviewer=self.request.user,
            auction_id=auction_id
            )


class CommentRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsOwnerOrAdmin]
    serializer_class = CommentSerializer

    def get_queryset(self):
        return Comment.objects.filter(auction_id=self.kwargs['auction_id'])


