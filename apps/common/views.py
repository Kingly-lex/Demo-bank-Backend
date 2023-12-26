# from rest_framework.response import Response
# from rest_framework import status
# from rest_framework.generics import GenericAPIView
# from rest_framework.permissions import IsAuthenticated


# # custom imports
# from .permissions import IsAdmin


# from .serializers import AccountGenerateSerializer


# class GenerateNewAccountNo(GenericAPIView):
#     permission_classes = [IsAuthenticated, IsAdmin]
#     serializer_class = AccountGenerateSerializer

#     def get(self, request):
#         data = self.serializer_class.get_account_no()
#         return Response(data, status=status.HTTP_201_CREATED)
