from rest_framework import serializers

# create a serializer
from lunch.models import Restaurant, Menu, LunchAppUser, Vote


class LunchAppUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = LunchAppUser
        fields = ('username', 'user_type')


class RestaurantSerializer(serializers.ModelSerializer):
    # initialize model and fields you want to serialize
    restaurant_owner = LunchAppUserSerializer(read_only=True)

    class Meta:
        model = Restaurant
        fields = ('name', "restaurant_owner")

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data["restaurant_owner"] = user
        print(validated_data)
        restaurant = Restaurant.objects.create(**validated_data)
        return restaurant


class MenuSerializer(serializers.ModelSerializer):
    restaurant = RestaurantSerializer(read_only=True)

    class Meta:
        model = Menu
        fields = ['name', 'type', 'restaurant', 'day', 'items']

    def create(self, validated_data):
        """
        Create function for menu and the restaurant is associated. The restaurantId
        is taken from the corresponding path parameter and the ingredients can be added optionally in the post body.
        """
        print("restaurant:", validated_data)
        menu = Menu.objects.create(**validated_data)
        return menu


class VoteSerializer(serializers.ModelSerializer):
    employee = LunchAppUserSerializer(read_only=True)

    class Meta:
        model = Vote
        fields = ['employee', 'menu', 'vote']

    def create(self, validated_data):
        vote = Vote.objects.create(**validated_data)
        return vote


class VotingResultSerializer(serializers.ModelSerializer):
    total = serializers.IntegerField()

    class Meta:
        model = Vote
        fields = ['menu_id', 'total']



