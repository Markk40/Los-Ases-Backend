from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from users.models import CustomUser 
# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=50, blank=False, unique=True)
    class Meta:
        ordering=('id',)
    def __str__(self):
        return self.name
    
class Auction(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    # rating = models.DecimalField(max_digits=3, decimal_places=2)
    stock = models.IntegerField(validators=[MinValueValidator(1)])
    brand = models.CharField(max_length=100)
    category = models.ForeignKey(Category, related_name='auctions', on_delete=models.CASCADE)
    thumbnail = models.ImageField(upload_to='fotos_coches/')
    creation_date = models.DateTimeField(auto_now_add=True)
    closing_date = models.DateTimeField()
    auctioneer = models.ForeignKey(CustomUser, related_name='auctions', on_delete=models.CASCADE)
    class Meta:
        ordering=('id',)
    def __str__(self):
        return self.title
    
    @property
    def average_rating(self):
        ratings = self.ratings.all()
        if ratings.exists():
            avg = sum(r.points for r in ratings) / ratings.count()
            return round(avg, 2)
        return 1.0 
    
class Bid(models.Model):
    auction = models.ForeignKey(Auction, related_name='bids', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    creation_date = models.DateTimeField(auto_now_add=True)
    bidder = models.ForeignKey(CustomUser, related_name='bids', on_delete=models.CASCADE)

    class Meta:
        ordering = ('id',)  # las pujas más recientes primero

    def __str__(self):
        return f"{self.bidder} - {self.price}€ en {self.auction.title}"

class Rating(models.Model):
    auction = models.ForeignKey(Auction, related_name='ratings', on_delete=models.CASCADE)
    reviewer = models.ForeignKey(CustomUser, related_name='ratings', on_delete=models.CASCADE)
    points = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])

    class Meta:
        unique_together = ('reviewer', 'auction')

    def __str__(self):
        return f"{self.reviewer.username} dio {self.points} a {self.auction.title}"
