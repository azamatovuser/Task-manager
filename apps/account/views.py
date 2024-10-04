from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from apps.account.models import Account, Friend
from apps.account.serializers import (TopAccountListSerializer,
                                      AccountDetailSerializer,
                                      FriendSerializer,
                                      RegisterSerializer,
                                      LoginSerializer,
                                      AccountSearchSerializer)
from django.db.models import Count, Q
from django.utils.timezone import now


class TopAccountAPIList(generics.ListAPIView):
    serializer_class = TopAccountListSerializer

    def get_queryset(self):
        today = now().date()
        user = self.request.user

        # Get IDs of friends of the requesting user
        friends_from_user = Friend.objects.filter(user=user).values_list('friend_id', flat=True)
        friends_from_friend = Friend.objects.filter(friend=user).values_list('user_id', flat=True)

        # Combine IDs and remove duplicates
        friend_ids = set(friends_from_user) | set(friends_from_friend)

        # Filter accounts to include only friends
        return Account.objects.filter(id__in=friend_ids).annotate(
            tasks_done_today=Count(
                'task',
                filter=Q(task__is_done=True) & Q(task__created_date__date=today)
            )
        ).order_by('-tasks_done_today')[:5]


class AccountAPIDetail(generics.RetrieveAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountDetailSerializer


class   AccountListAPIView(generics.ListAPIView):
    serializer_class = TopAccountListSerializer

    def get_queryset(self):
        today = now().date()
        user = self.request.user

        friends_from_user = Friend.objects.filter(user=user).values_list('friend_id', flat=True)
        friends_from_friend = Friend.objects.filter(friend=user).values_list('user_id', flat=True)

        friend_ids = set(friends_from_user) | set(friends_from_friend)

        return Account.objects.filter(id__in=friend_ids).annotate(
            tasks_done_today=Count(
                'task',
                filter=Q(task__is_done=True) & Q(task__created_date__date=today)
            )
        )

    def get_serializer_context(self):
        return {'request': self.request}


class AccountSearchListAPIView(generics.ListAPIView):
    serializer_class = AccountSearchSerializer

    def get_queryset(self):
        search = self.request.GET.get('search')
        if search:
            return Account.objects.filter(username__icontains=search)
        return Account.objects.all()


class FriendRemoveAPIView(generics.DestroyAPIView):
    queryset = Friend.objects.all()
    serializer_class = FriendSerializer


class FriendAddAPIView(generics.CreateAPIView):
    queryset = Friend.objects.all()
    serializer_class = FriendSerializer
    permission_classes = (IsAuthenticated, )


# REGISTRATION AND LOGIN

class AccountRegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        username = serializer.data.get('username')
        tokens = Account.objects.get(username=username).tokens
        user_data['tokens'] = tokens
        return Response({'success': True, 'data': user_data}, status=status.HTTP_201_CREATED)



class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'success': True, 'data': serializer.data}, status=status.HTTP_200_OK)