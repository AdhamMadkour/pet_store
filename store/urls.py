from rest_framework import routers
from rest_framework_nested import routers
from .views import (
    AuctionViewSet,
    BidViewSet,
    PetBidViewSet,
    PetViewSet,
    StorePetViewSet,
)


router = routers.DefaultRouter()
router.register("pets", PetViewSet, basename="Pets")
router.register("store", StorePetViewSet, basename="Store")
router.register("auction", AuctionViewSet, basename="Auction")
router.register("bid", BidViewSet, basename="Bid")

router_pet = routers.NestedDefaultRouter(router, "pets", lookup="pet")
router_pet.register("bids", PetBidViewSet, basename="pet-bids")

urlpatterns = router.urls + router_pet.urls
