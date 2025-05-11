from django.urls import path
from .views import (CategoryListCreate, CategoryRetrieveUpdateDestroy, 
                    AuctionListCreate, AuctionRetrieveUpdateDestroy, 
                    BidListCreate, BidRetrieveUpdateDestroy, 
                    UserAuctionListView, RatingListCreate, RatingRetrieveUpdateDestroy)
app_name="auctions"
urlpatterns = [
    path('categories/', CategoryListCreate.as_view(), name='category-list-create'),
    path('categories/<int:pk>/', CategoryRetrieveUpdateDestroy.as_view(), name='category-detail'),
    path('', AuctionListCreate.as_view(), name='auction-list-create'),
    path('<int:pk>/', AuctionRetrieveUpdateDestroy.as_view(), name='auction-detail'),
    path('<int:auction_id>/bid/', BidListCreate.as_view(), name='bid-list-create'),
    path('<int:auction_id>/bid/<int:pk>/', BidRetrieveUpdateDestroy.as_view(), name='bid-detail'),
    path('users/', UserAuctionListView.as_view(), name='action-from-users'),
    path('<int:auction_id>/ratings/', RatingListCreate.as_view(), name='rating-list-create'),
    path('<int:auction_id>/ratings/<int:pk>/', RatingRetrieveUpdateDestroy.as_view(), name='rating-detail'),
]