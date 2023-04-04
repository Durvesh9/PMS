# '''
# from rest_framework import generics
# from rest_framework.response import Response
# from rest_framework.decorators import api_view
# from .models import Medicine
# from .serializers import MedicineSerializer

# @api_view(['GET'])
# def medicine_list(request):
#     medicines = Medicine.objects.all()
#     serializer = MedicineSerializer(medicines, many=True)
#     return Response(serializer.data)

# @api_view(['GET'])
# def medicine_detail(request, pk):
#     medicine = Medicine.objects.get(pk=pk)
#     serializer = MedicineSerializer(medicine)
#     return Response(serializer.data)

# @api_view(['POST'])
# def medicine_create(request):
#     serializer = MedicineSerializer(data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data, status=201)
#     return Response(serializer.errors, status=400)

# @api_view(['PUT'])
# def medicine_update(request, pk):
#     medicine = Medicine.objects.get(pk=pk)
#     serializer = MedicineSerializer(medicine, data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data)
#     return Response(serializer.errors, status=400)

# @api_view(['DELETE'])
# def medicine_delete(request, pk):
#     medicine = Medicine.objects.get(pk=pk)
#     medicine.delete()
#     return Response(status=204)
# '''

# from django.shortcuts import render, HttpResponse
# from django.contrib import messages
# from django.contrib.auth.models import User
# from django.contrib.auth import authenticate
# # def project()

# def project(request):
#     return render(request,"Project.html")


# # def login(request):
# #     if request.method == 'POST':
# #         username =  request.POST['username']
# #         password =  request.POST['password']

# #         user = authenticate(username=username, password=password)

# #         if user is not None:
# #             login(request, user)
# #             return render(request, "Project.html")
# #         else:
# #             messages.error(request, "Invalid credentials")
# #             return redirect('login')
# #         return render(request,"login.html")
        






# #     return render(request, "login.html")