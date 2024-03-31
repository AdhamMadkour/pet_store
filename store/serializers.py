from django.utils import timezone
from .models import Auction, Bid, Pet
from rest_framework import serializers


class CreatePetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pet
        fields = [
            "id",
            "name",
            "age",
            "status",
            "price",
            "category",
            "tags",
        ]


class PetSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField()
    tags = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    owner = serializers.SerializerMethodField(read_only=True)
    bidders = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Pet
        fields = [
            "id",
            "owner",
            "name",
            "age",
            "status",
            "price",
            "created_at",
            "updated_at",
            "category",
            "tags",
            "bidders",
        ]

    def get_category(self, obj):
        return {
            "id": obj.category.id,
            "name": obj.category.name,
        }

    def get_tags(self, obj):
        return [{"id": tag.id, "name": tag.name} for tag in obj.tags.all()]

    def get_status(self, obj):
        return "available" if obj.status else "sold"

    def get_owner(self, obj):
        return {
            "id": obj.owner.id,
            "username": obj.owner.username,
        }

    def get_bidders(self, obj):
        if hasattr(obj, "auction"):
            return [
                {
                    "id": bid.bidder.id,
                    "username": bid.bidder.username,
                    "price": bid.price,
                }
                for bid in obj.auction.bid_set.all()
            ]
        return []


class StorePetSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField()
    tags = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    owner = serializers.SerializerMethodField()
    isForAuction = serializers.SerializerMethodField()

    class Meta:
        model = Pet
        fields = [
            "id",
            "name",
            "age",
            "status",
            "price",
            "category",
            "tags",
            "owner",
            "isForAuction",
        ]

    def get_owner(self, obj):
        return {
            "id": obj.owner.id,
            "username": obj.owner.username,
        }

    def get_category(self, obj):
        return {
            "id": obj.category.id,
            "name": obj.category.name,
        }

    def get_tags(self, obj):
        return [{"id": tag.id, "name": tag.name} for tag in obj.tags.all()]

    def get_status(self, obj):
        return "available" if obj.status else "sold"

    def get_isForAuction(self, obj):
        has_auction = hasattr(obj, "auction")
        if has_auction:
            return {
                "id": obj.auction.id,
                "number_of_bids": obj.auction.bid_set.count(),
                "start_price": obj.auction.start_price,
                "start_date": obj.auction.start_date,
                "end_date": obj.auction.end_date,
            }
        return False


class AuctionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Auction
        fields = [
            "id",
            "pet",
            "start_price",
            "start_date",
            "end_date",
            "created_at",
            "updated_at",
        ]

    def create(self, validated_data):
        pet = validated_data["pet"]
        if pet.status and pet.owner == self.context["request"].user:
            return super().create(validated_data)
        raise serializers.ValidationError(
            "Pet is not available or you are not the owner"
        )

    def update(self, instance, validated_data):
        pet = validated_data.get("pet")
        if pet.status and pet.owner == self.context["request"].user:
            return super().update(instance, validated_data)
        raise serializers.ValidationError(
            "Pet is not available or you are not the owner"
        )

    def delete(self, instance):
        if instance.pet.status and instance.pet.owner == self.context["request"].user:
            return super().delete(instance)
        raise serializers.ValidationError(
            "Pet is not available or you are not the owner"
        )


class BidSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bid
        fields = [
            "id",
            "auction",
            "price",
            "created_at",
            "updated_at",
        ]

    def create(self, validated_data):
        auction = validated_data["auction"]

        # check if the user is not the owner of the pet
        if auction.pet.owner == self.context["request"].user:
            raise serializers.ValidationError("You can't bid on your own pet")

        # check if there is auction for this pet
        if not hasattr(auction.pet, "auction"):
            raise serializers.ValidationError("There is no auction for this pet")

        # check if the auction is still open
        if auction.end_date < timezone.now():
            raise serializers.ValidationError("The auction is closed")

        # check if the user did not bid on this auction before

        if auction.bid_set.filter(bidder=self.context["request"].user).exists():
            raise serializers.ValidationError("You already bid on this auction")

        # check if the price is higher than the start price
        if validated_data["price"] < auction.start_price:
            raise serializers.ValidationError(
                "The price must be higher than the start price"
            )

        bidder = self.context["request"].user
        bid = Bid.objects.create(bidder=bidder, **validated_data)
        return bid

    def update(self, instance, validated_data):
        auction = instance.auction

        if auction.pet.owner == self.context["request"].user:
            raise serializers.ValidationError("You can't bid on your own pet")

        if auction.end_date < timezone.now():
            raise serializers.ValidationError("The auction is closed")

        if validated_data["price"] < auction.start_price:
            raise serializers.ValidationError(
                "The price must be higher than the start price"
            )

        instance.price = validated_data["price"]
        instance.save()
        return instance
