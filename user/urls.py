from django.urls import path
from .views import SimpleScrapeView, DetailedScrapeView

urlpatterns = [
    path('simple-scrape/', SimpleScrapeView.as_view(), name='simple_scrape'),
    path('detailed-scrape/', DetailedScrapeView.as_view(), name='detailed_scrape'),
]