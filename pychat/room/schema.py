from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from .serializer import RoomSerializer, ChannelSerializer



room_list_docs = extend_schema(
    responses=RoomSerializer(many=True),
    parameters=[
        OpenApiParameter(
            name='category',
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            description='Category of rooms to retrieve',
        ),
        OpenApiParameter(
            name='qty',
            type=OpenApiTypes.INT,
            location=OpenApiParameter.QUERY,
            description='Limits the number of rooms to retrieve ',
        ),
        OpenApiParameter(
            name='by_user',
            type=OpenApiTypes.BOOL,
            location=OpenApiParameter.QUERY,
            description='filters the rooms based on the authenticated User',
        ),
        OpenApiParameter(
            name='by_roomId',
            type=OpenApiTypes.INT,
            location=OpenApiParameter.QUERY,
            description='Filters the rooms by a specific room ID',
        ),
        OpenApiParameter(
            name='with_num_members',
            type=OpenApiTypes.INT,
            location=OpenApiParameter.QUERY,
            description='Includes the number of members in each room.',
        ),
        OpenApiParameter(
            name='by_roomId',
            type=OpenApiTypes.INT,
            location=OpenApiParameter.QUERY,
            description='Includes room by id',
        ),
        
    ],

)