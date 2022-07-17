from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum
from django.http import Http404, HttpResponseForbidden
from django.shortcuts import render, redirect

# Create your views here.
from rest_framework import viewsets, views, status
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import BrowsableAPIRenderer, JSONRenderer, HTMLFormRenderer
from rest_framework.response import Response

from lunch.forms import LunchAppUserCreationForm
from lunch.models import Restaurant, Menu, Vote
from lunch.permissions import EmployeePermission, RestaurantOwnerPermission
from lunch.serializers import RestaurantSerializer, MenuSerializer, VoteSerializer, VotingResultSerializer


class RestaurantViewSet(viewsets.ModelViewSet):
    # define queryset
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = [IsAuthenticated, RestaurantOwnerPermission]


class Menus(views.APIView):
    serializer_class = MenuSerializer
    renderer_classes = (BrowsableAPIRenderer, JSONRenderer, HTMLFormRenderer)

    def get(self, request):
        user = request.user
        if user.user_type == 'restaurant_owner':
            menus = Menu.objects.filter(restaurant__restaurant_owner=user)
        elif user.user_type == 'employee':
            menus = Menu.objects.all()
        serializer = MenuSerializer(menus, many=True)
        return Response(serializer.data)

    def post(self, request):
        user = request.user
        if user.user_type == 'restaurant_owner':
            try:
                restaurant = Restaurant.objects.get(restaurant_owner=request.user)
            except Restaurant.DoesNotExist:
                return Response({"detail": "LunchAppUser has no Restaurant"}, status=status.HTTP_404_NOT_FOUND)

            serializer = MenuSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(restaurant=restaurant)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"detail": "Permission denied. Employee can not add menu"},
                            status=status.HTTP_403_FORBIDDEN)


class VoteView(views.APIView):
    serializer_class = VoteSerializer
    renderer_classes = (BrowsableAPIRenderer, JSONRenderer, HTMLFormRenderer)

    def get(self, request):
        votes = Vote.objects.all()
        serializer = VoteSerializer(votes, many=True)
        return Response(serializer.data)

    def post(self, request):
        user = request.user
        if user.user_type == 'employee':
            serializer = VoteSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(employee=request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"detail": "Permission denied. Restaurant owners can not vote for menu"},
                            status=status.HTTP_403_FORBIDDEN)


class VotingResults(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed voting results
    """
    queryset = Vote.objects.values("menu_id").annotate(total=Sum("vote")).order_by('total').reverse()
    serializer_class = VotingResultSerializer


def register_request(request):
    if request.method == "POST":
        form = LunchAppUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("/restaurant")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = LunchAppUserCreationForm()
    return render(request=request, template_name="registration/register.html", context={"register_form": form})

