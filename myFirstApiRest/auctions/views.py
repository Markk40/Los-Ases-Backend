from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from .models import Category, Auction, Bid
from .serializers import CategoryListCreateSerializer, CategoryDetailSerializer, AuctionListCreateSerializer, AuctionDetailSerializer, BidListCreateSerializer, BidDetailSerializer
from rest_framework.views import APIView 
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from .permissions import IsOwnerOrAdmin 

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
    queryset = Auction.objects.all()
    serializer_class = AuctionListCreateSerializer
    
class AuctionRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsOwnerOrAdmin]
    queryset = Auction.objects.all()
    serializer_class = AuctionDetailSerializer

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