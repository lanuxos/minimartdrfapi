from .models import Item
from .serializers import ItemSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import serializers, status
from django.shortcuts import get_object_or_404

from api import serializers

@api_view(['GET'])
def apiOverview(request):
    api_urls = {
        'All_items': '/',
        'Search by category': '/?category=category_name',
        'Search by subcategory': '/?subcategory=category_name',
        'Add': '/create',
        'Update': '/update/pk',
        'Delete': '/item/pk/delete'
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


@api_view(['POST'])
def updateItems(request, pk):
    item = Item.objects.get(pk=pk)
    data = ItemSerializer(instance=item, data=request.data)

    if data.is_valid():
        data.save()
        return Response(data.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)
    

@api_view(['PUT'])
def updatePartialItems(request, pk):
    keys = ['category', 'subcategory', 'name', 'amount']
    item = Item.objects.get(pk=pk)
    updateData = {}
    updateData['category'] = item.category
    updateData['subcategory'] = item.subcategory
    updateData['name'] = item.name
    updateData['amount'] = item.amount
    for k in keys:
        if k in request.data:
            updateData[k] = request.data[k]

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