from rest_framework.response import Response
from rest_framework import generics, viewsets
from django.db.models import Q
from django.shortcuts import get_object_or_404

from ..models import Network, Organisation, Method, CustomUser, Survey
from ..serializers import NetworkSerializer, OrganisationSerializer


class NetworkViewSet(viewsets.ModelViewSet):
    serializer_class = NetworkSerializer
   
    ''' GET Request '''
    def get_queryset(self):
        mynetworks = self.request.GET.get('mynetworks', None)
        allnetworks = self.request.GET.get('allnetworks', None)
        organisation = self.request.GET.get('organisation', None)
        excludeorganisation = self.request.GET.get('excludeorganisation', None)
        
        if mynetworks is not None:
            return Network.objects.filter(teammembers__user=self.request.user)
        if allnetworks is not None:
            if self.request.user.is_superuser:
                return Network.objects.all()
            else:
                return Network.objects.filter(Q(teammembers__user=self.request.user) | Q(ispublic = True)).distinct()
        if organisation is not None:
            return Network.objects.filter(organisations=organisation)
        if excludeorganisation is not None:
            return Network.objects.exclude(Q(organisations=excludeorganisation) | Q(memberships__organisation=excludeorganisation))
        return Network.objects.all() # filter(teammembers__user=self.request.user)
    
    ''' POST request '''
    def create(self, request):
        serializer = NetworkSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save(created_by=request.user)
        return Response(serializer.data)













    # def update(self, request, *args, **kwargs):
    # #     return super().update(request, *args, **kwargs)
    #     networkobject = self.get_object() #get_object_or_404(Network, pk=pk)
    #     print('>>>', request.data)
    #     print(networkobject)
     
    #     serializer = NetworkSerializer(networkobject, data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     print('test', serializer.data)
    #     return Response(serializer.data)

'''
Shouldn't i change partial update with update?
'''
   # if not 'surveys' in request.data[0].keys():
        #     for instance in request.data:
        #         try: 
        #             organisation = get_object_or_404(Organisation, name=instance['name'])
        #             if networkobject.organisations.filter(name=organisation.name).exists():
        #                 networkobject.organisations.remove(organisation)
        #             else:
        #                 networkobject.organisations.add(organisation)
        #         except Exception as e:
        #             return Response({'error': f'{e}'})
        #             # print('%s (%s)' % (type(e)))
        # else:
        #     for instance in request.data:
        #         print('>>>', instance)
        #         try: 
        #             method = get_object_or_404(Method, pk=instance['id'])
        #             print(method)
        #             if networkobject.methods.filter(name=method.name).exists():
        #                 networkobject.methods.remove(method)
        #             else:
        #                 networkobject.methods.add(method)
        #         except Exception as e:
        #             return Response({'error': f'{e}'})
        #             print(f'{type(e)}') #print('%s (%s)' % (e.message, type(e)))