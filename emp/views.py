from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from emp.models import User, Employee, Role
from emp.serializers import UserSerializer, EmployeeSerializer, UserSerializer1


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")
    if not username:
        return Response({'username': 'Please provide username'})
    if not password:
        return Response({'password': 'Please provide password'})

    user = authenticate(username=username, password=password)

    if not user:
        return Response({'invalid_credential': 'Please provide valid credential'})

    token, _ = Token.objects.get_or_create(user=user)

    return Response({'token': token.key, 'user_id': user.id, 'role_id': user.role_id})


class EmployeeViewSet(viewsets.ModelViewSet):

    serializer_class = UserSerializer
    queryset = User.objects.all()

    def create(self, request, *args, **kwargs):

        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            role = Role.objects.get(name='Admin')
            if user.role_id == role.id:
                user = User.objects.filter(username=serializer.validated_data['username'])
            if not user:
                res = serializer.save()
                res.set_password(serializer.validated_data['password'])
                res.save()

                Employee.objects.create(user_id=res.id,
                                        emp_id=request.data.get('emp_id'),
                                        address=request.data.get('address'),
                                        gender=request.data.get('gender'))

                return Response({'successfully added'})

            else:
                return Response({'You dont have permission to add'})
        return Response(serializer.errors)

    def partial_update(self, request, pk=None, *args, **kwargs):
        user = request.user
        role = Role.objects.get(name='Admin')

        if user.role_id == role.id:
            res = User.objects.get(id=pk)
            if res:
                serializer = UserSerializer(instance=res, data=request.data, partial=True)
                if serializer.is_valid():
                    res = serializer.save()
                    res.set_password(serializer.validated_data['password'])
                    res.save()

                    res1 = Employee.objects.get(user_id=res.id)
                    if res1:
                        serializer1 = EmployeeSerializer(instance=res1, data=request.data, partial=True)
                        if serializer1.is_valid():
                            res1 = serializer1.save()
                            return Response({'Updated': 'successfully'})
                return Response(serializer.errors)
        return Response({'You dont have permission to update'})

    def destroy(self, request, pk=None, *args, **kwargs):
        user = request.user
        role = Role.objects.get(name='Admin')

        if user.role_id == role.id:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response({'Deleted': 'successfully'})
        return Response({'You dont have permission to delete'})




