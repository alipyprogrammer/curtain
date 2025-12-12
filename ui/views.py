from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from .serializer import *


@api_view(['GET'])
def page(request, pk):
    dic_send = {}

    get_home_obj = get_object_or_404(Page, idd=pk, status=True)

    get_header_serializer = NavBarSerializer(get_home_obj.header)
    get_slider_serializer = SliderSerializer(get_home_obj.slider.filter(status=True), many=True)
    get_banner_serializer = BannerSerializer(get_home_obj.banner.filter(status=True), many=True)
    get_suggestion_box_serializer = BoxSerializer(get_home_obj.box, many=True)


    dic_send['header'] = get_header_serializer.data
    dic_send['slider'] = get_slider_serializer.data
    dic_send['banner'] = get_banner_serializer.data
    dic_send['box'] = get_suggestion_box_serializer.data

    return Response({
            "status": True,
            "message": "done",
            "data": dic_send
        }, status=200)


