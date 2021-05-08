from rest_framework.response import Response
from rest_framework import generics, viewsets
from django.db.models import Q
from django.shortcuts import get_object_or_404

from ..models import Network, Organisation, Method, CustomUser, Survey
from ..serializers import NetworkSerializer, OrganisationSerializer


class NetworkViewSet(viewsets.ModelViewSet):
    serializer_class = NetworkSerializer
   
    def get_queryset(self):
        organisation = self.request.GET.get('organisation', None)
        excludeorganisation = self.request.GET.get('excludeorganisation', None)
        if organisation is not None:
            return Network.objects.filter(organisations=organisation)
        if excludeorganisation is not None:
            return Network.objects.exclude(organisations=excludeorganisation)
        return Network.objects.filter(Q(created_by=self.request.user) | Q(ispublic = True))
    
    def create(self, serializer):
        serializer = NetworkSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(created_by=self.request.user)
        return Response(serializer.data)

    def partial_update(self, request, pk):
        networkobject = get_object_or_404(Network, pk=pk)
        print('>>>', request.data)
        if not 'surveys' in request.data[0].keys():
            for instance in request.data:
                try: 
                    organisation = get_object_or_404(Organisation, name=instance['name'])
                    if networkobject.organisations.filter(name=organisation.name).exists():
                        networkobject.organisations.remove(organisation)
                    else:
                        networkobject.organisations.add(organisation)
                except Exception as e:
                    return Response({'error': f'{e}'})
                    # print('%s (%s)' % (type(e)))
        else:
            for instance in request.data:
                print('>>>', instance)
                try: 
                    method = get_object_or_404(Method, pk=instance['id'])
                    print(method)
                    if networkobject.methods.filter(name=method.name).exists():
                        networkobject.methods.remove(method)
                    else:
                        networkobject.methods.add(method)
                except Exception as e:
                    return Response({'error': f'{e}'})
                    print(f'{type(e)}') #print('%s (%s)' % (e.message, type(e)))
        serializer = NetworkSerializer(networkobject)
        return Response(serializer.data)

'''
Shouldn't i change partial update with update?
'''