from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .permissions import IsOwnerOfThePet, OwnerOnly
from .models import Bid, Pet, Auction
from .serializers import (
    AuctionSerializer,
    CreatePetSerializer,
    PetSerializer,
    StorePetSerializer,
    BidSerializer,
)


class PetViewSet(viewsets.ModelViewSet):
    serializer_class = PetSerializer

    def get_serializer_class(self):
        if self.action == "create":
            return CreatePetSerializer
        return PetSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
        return super().perform_create(serializer)

    def get_permissions(self):
        if self.action == "create":
            return [IsAuthenticated()]
        if self.action in ["update", "partial_update", "destroy"]:
            return [IsAuthenticated(), OwnerOnly()]
        return [IsAuthenticated()]

    def get_queryset(self):
        return (
            Pet.objects.filter(owner=self.request.user)
            .select_related("owner")
            .select_related("category")
            .prefetch_related("tags")
        )


class StorePetViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = StorePetSerializer
    queryset = (
        Pet.objects.filter(status=True)
        .select_related("owner")
        .select_related("category")
        .prefetch_related("tags")
    )


class AuctionViewSet(viewsets.ModelViewSet):
    serializer_class = AuctionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Auction.objects.filter(pet__owner=self.request.user)


class BidViewSet(viewsets.ModelViewSet):
    queryset = Bid.objects.all()
    serializer_class = BidSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Bid.objects.filter(bidder=self.request.user)


class PetBidViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Bid.objects.all()
    serializer_class = BidSerializer

    def get_queryset(self):
        if self.request.user.is_anonymous:
            return Bid.objects.none()
        return (
            Bid.objects.filter(auction__pet__owner=self.request.user)
            .filter(auction__pet=self.kwargs["pet_pk"])
            .select_related("auction")
            .select_related("bidder")
        )

    def get_permissions(self):
        if self.request.user.is_anonymous:
            return [IsAuthenticated()]
        return [IsOwnerOfThePet(), IsAuthenticated()]
