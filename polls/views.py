from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from polls.serializers import PollSerializer
from polls.models import Poll

@api_view(['GET','POST'])
def index(request):
    if request.method == "POST":
        serializer = PollSerializer(data = request.data)
        if not serializer.is_valid():
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    if request.method == "GET":
        if request.GET.get('order'):
            order = request.GET.get('order')
        else:
            order = "latest"

        if order == "latest":
            polls = Poll.objects.all().order_by('-createAt')
        elif order == "oldest":
            polls = Poll.objects.all().order_by('createAt')
        elif order == "agree":
            polls = Poll.objects.all().order_by('-agree')
        else:
            polls = Poll.objects.all().order_by('-disagree')

        serializer = PollSerializer(polls,many=True)
        return Response(serializer.data)

@api_view(['GET','PUT','DELETE'])
def poll_detail(request,id):
    poll = get_object_or_404(Poll,pk=id)
    if request.method == 'GET':
        serializer = PollSerializer(poll)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = PollSerializer(poll,data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.data,status=status.HTTP_200_OK)
    else:
        serializer = PollSerializer(poll)
        poll.delete()
        return Response(serializer.data,status=status.HTTP_200_OK)
    
@api_view(['POST'])    
def poll_agree(request,id):
    poll = get_object_or_404(Poll,pk=id)
    poll.agree = poll.agree + 1
    poll.agreeRate = poll.agree/(poll.agree + poll.disagree)
    poll.disagreeRate = poll.disagree/(poll.agree + poll.disagree)
    serializer = PollSerializer(poll)
    poll.save()
    serializer = PollSerializer(poll)
    return Response(serializer.data,status=status.HTTP_200_OK)

@api_view(['POST'])    
def poll_disagree(request,id):
    poll = get_object_or_404(Poll,pk=id)
    poll.disagree = poll.disagree + 1
    poll.agreeRate = poll.agree/(poll.agree + poll.disagree)
    poll.disagreeRate = poll.disagree/(poll.agree + poll.disagree)
    serializer = PollSerializer(poll)
    poll.save()
    serializer = PollSerializer(poll)
    return Response(serializer.data,status=status.HTTP_200_OK)