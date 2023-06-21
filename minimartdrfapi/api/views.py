from .models import Item
from .serializers import ItemSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import serializers, status
from django.shortcuts import get_object_or_404

from api import serializers


@api_view(['GET'])
def apiOverview(request):
    if request.user.is_authenticated:
        api_urls = {
            'All_items': '/',
            'Search by category': '/?category=category_name',
            'Search by subcategory': '/?subcategory=category_name',
            'Add': '/create',
            'Update': '/update/pk',
            'Delete': '/item/pk/delete'
        }
    else:
        api_urls = {
            'All_items': '/',
            'Search by category': '/?category=category_name',
            'Search by subcategory': '/?subcategory=category_name'
        }

    return Response(api_urls)

@api_view(['POST'])
def addItems(request):
    item = ItemSerializer(data=request.data)

    if Item.objects.filter(**request.data).exists():
        raise serializers.ValidationError('This data already existed')
    
    if item.is_valid():
        item.save()
        return Response(item.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)
    

@api_view(['GET'])
def viewItems(request):
    if request.query_params:
        items = Item.objects.filter(**request.query_params.dict())
    else:
        items = Item.objects.all()

    if items:
        serializer = ItemSerializer(items, many=True)
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)
    '''
    localhost:8000/api/all
    localhost:8000/api/?category=category_name
    localhost:8000/api/?subcategory=subcategory_name
    localhost:8000/api/all/?name=name
    localhost:8000/api/all/?category=category
    '''


@api_view(['POST', 'PUT'])
def updateItems(request, pk):
    if request.method == 'POST':
        item = Item.objects.get(pk=pk)
        data = ItemSerializer(instance=item, data=request.data)

        if data.is_valid():
            data.save()
            return Response(data.data)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
    elif request.method == 'PUT':
        updateData = {}
        item = Item.objects.get(pk=pk)
        for key in item.__dict__: # convert item object into dictionary and iterate
            if not key.startswith("_"):
                if key in request.data:
                    updateData[key] = request.data[key]
                else:
                    updateData[key] = getattr(item, key)

        data = ItemSerializer(instance=item, data=updateData)
        if data.is_valid():
            data.save()
            return Response(data.data)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['DELETE'])
def deleteItems(request, pk):
    item = get_object_or_404(Item, pk=pk) # from django.shortcuts import get_object_or_404
    item.delete()
    return Response(status=status.HTTP_202_ACCEPTED)