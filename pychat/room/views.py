from rest_framework import viewsets
from .models import Room
from .serializer import RoomSerializer
from django.db.models import Count
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError, AuthenticationFailed
from .schema import room_list_docs


class RoomListViewSet(viewsets.ViewSet):
    # Set the initial queryset to retrieve all Room objects
    queryset = Room.objects.all()

    @room_list_docs
    def list(self, request):
        """
         Retrieves a list of rooms based on the provided query parameters.

    This method filters the list of rooms based on various query parameters and returns the serialized room data.

    Args:
        request (rest_framework.request.Request): The incoming HTTP request object.

    Raises:
        AuthenticationFailed: If the user is not authenticated but the query parameters require authentication.

    Returns:
        rest_framework.response.Response: The HTTP response containing the serialized room data.

    Query Parameters:
        category (str, optional): Filters the rooms by category name.
        qty (int, optional): Limits the number of rooms returned.
        by_user (bool, optional): If True, filters the rooms based on the authenticated user.
        by_roomId (int, optional): Filters the rooms by a specific room ID.
        with_num_members (bool, optional): If True, includes the number of members in each room.

    Raises:
        ValidationError: If the provided query parameters are invalid or the requested room ID does not exist.
    
    Usage:
        This method can be used to retrieve a list of rooms based on the provided query parameters. The query parameters can be used to filter the rooms by category, limit the number of rooms, filter by user membership, filter by room ID, and include the count of members in each room.

        Example:
            GET /rooms/?category=private&qty=10&by_user=true&with_num_members=true

        This example will retrieve a list of private rooms where the current user is a member. The response will include a maximum of 10 rooms, and each room will be annotated with the count of members.
    Note:
        - If both `by_user` and `by_roomId` are present in the query parameters, authentication is required.
        - If `qty` is not provided, all rooms matching the other criteria will be returned.
        - If `with_num_members` is True, each room will include a field indicating the number of members in it.
        """

         # Get the "category" query parameter from the request
        category = request.query_params.get("category")

        # Get the "qty" query parameter from the request
        qty = request.query_params.get("qty")

        # Check if the "by_user" query parameter is "true"
        by_user = request.query_params.get('by_user') == "true"

        # Get the value of the "by_roomId" query parameter from the request
        by_roomId = request.query_params.get('by_rommId')

        # Check if the "with_num_members" query parameter is "true"
        with_num_members = request.query_params.get('with_num_members') == "true"

        # Check authentication for "by_user" or "by_roomId" queries
        if by_user or by_roomId and not request.user.is_authenticated:
            raise AuthenticationFailed()
        
        # Filter the queryset based on the "category" query parameter
        if category:
            self.queryset = self.queryset.filter(category__name = category)

        # Filter the queryset to include only rooms where the current user is a member
        if by_user:
            user_id = request.user.id
            self.queryset =self.queryset.filter(member = user_id)

        # Annotate the queryset with the count of members in each room
        if with_num_members :
            self.queryset = self.queryset.annotate(num_members=Count("member"))

        # Filter the queryset based on the "by_roomId" query parameter
        if by_roomId:
            try:
                self.queryset = self.queryset.filter(id=by_roomId)
                # Check if the room with the given ID exists
                if not self.queryset.exists():
                    raise ValidationError(detail=f"Server with id {by_roomId} not found!")
            except ValueError:
                raise ValidationError(detail=f"Server value error!")
            
        # Limit the number of rooms in the queryset based on the "qty" query parameter    
        if qty:
            self.queryset = self.queryset[: int(qty)]
        # Serialize the queryset into JSON data using RoomSerializer
        serializer = RoomSerializer(self.queryset, many=True, context={"num_members":with_num_members })

        # Return the serialized data as a response
        return Response(serializer.data)
        
