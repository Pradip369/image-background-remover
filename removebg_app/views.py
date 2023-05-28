from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser,FormParser
from rest_framework import status
from .serializers import FastBGRemoveSerializer,SlowBGRemoveSerializer
# from .helper import fast_bg_remover
# from .helper import slow_bg_remover
import base64
from rest_framework.throttling import AnonRateThrottle


class FastRemove(APIView):

    parser_classes = [MultiPartParser, FormParser]
    throttle_classes = [AnonRateThrottle]

    def post(self, request, *args, **kwargs):
        serializer = FastBGRemoveSerializer(data = request.data)
        print(request.META.get('HTTP_ORIGIN'),">>>>>>>>>>>>>>>> host")
        if serializer.is_valid(raise_exception = True):
            ...
        #     try:
        #         final_image = fast_bg_remover.fast_remover(
        #             my_image = serializer.validated_data.get('image')
        #         )
        #         encodeded_img = 'data:image/png;base64,' + base64.b64encode(final_image).decode('ascii')
        #         return Response({"data" : encodeded_img}, status = status.HTTP_200_OK)
        #     except Exception as e:
        #         print(e,"errrrrr >>>>>>>>>>>>>")
        return Response("Something went wrong!!", status=status.HTTP_400_BAD_REQUEST)

class SlowRemove(APIView):

    parser_classes = [MultiPartParser, FormParser]
    throttle_classes = [AnonRateThrottle]

    def post(self, request, *args, **kwargs):
        serializer = SlowBGRemoveSerializer(data = request.data)
        if serializer.is_valid(raise_exception = True):
            data = serializer.validated_data
            try:
                final_image = slow_bg_remover.slow_remover(
                    my_image = data.get('image'),
                    is_grey = data.get('is_grey'),
                    is_blur = data.get('is_blur'),
                    blur_type = data.get('blur_type'),
                    detect = data.get('detect'),
                    )
                encodeded_img = 'data:image/png;base64,' + base64.b64encode(final_image).decode('ascii')
                return Response({"data" : encodeded_img}, status = status.HTTP_200_OK)
            except Exception as e:
                print(e,"err>>>>>>>>>>>>>")
        return Response("Something went wrong!!", status=status.HTTP_400_BAD_REQUEST)