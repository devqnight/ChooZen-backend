from choozenREST.imdb import search_movie_by_title, advanced_search_movie_by_title, advanced_search_movie_id, get_character_name, get_actor_picture, save_movie_in_db
from choozenREST.serializers import CustomGenreSerializer, MovieSerializer, CustomGroupListSerializer, GroupUserDetailsSerializer
from django.http import JsonResponse
from django.http.response import HttpResponse
from django.middleware.csrf import get_token
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework.viewsets import ModelViewSet

from .models import Directed, Genre, GroupLevel, HasGenre, HasProposed, IsPartOf, MemberLevel, Movie, Person, Played, User, GroupList

ERROR_POST_REQUIRED = "Only POST requests are allowed"
ERROR_GET_REQUIRED = "Only GET requests are allowed"

ERROR_USER_REQUIRED = "User ID is required"
ERROR_GROUP_REQUIRED = "Group ID is required"

ERROR_USER_NOT_EXIST = 'User does not exist'
ERROR_GROUP_NOT_EXIST = "Group does not exist"

ERROR_USER_NOT_IN_GROUP = 'User is not part of this group'

class MovieViewSet(ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    # permission_classes = [IsAuthenticated]

@csrf_exempt
def search_movie(request):
    if request.method == 'POST':
        title_requested = request.POST.get('movie-title')
        result = search_movie_by_title(title_requested)
        return HttpResponse(result)


def advanced_search_movie(request):
    if request.method == 'POST':
        title_requested = request.POST.get('movie-title')
        result = advanced_search_movie_by_title(title_requested)
        return HttpResponse(result)

def get_csrf(request):
    try:
      token = request.COOKIES['csrftoken']
    except KeyError:
      token = get_token(request)
    return HttpResponse(token)

@csrf_exempt
def is_authenticated(request):
    if request.method == 'POST':
      username = request.POST.get('username')
      token = request.POST.get('token')
      try:
        user = User.objects.get(username=username)
        token_db = Token.objects.get(key=token)
        if user.id == token_db.user_id:
          data = {'authenticated': True}
          data['id'] = user.id
          data['username'] = user.username
          data['first_name'] = user.first_name
          data['last_name'] = user.last_name
          data['email'] = user.email
          data['birthdate'] = user.birthdate
          data['last_login'] = user.last_login
          data['date_joined'] = user.date_joined
          data['is_superuser'] = user.is_superuser
          data['is_staff'] = user.is_staff
          data['is_active'] = user.is_active
          data['group_level_id'] = user.group_level_id
          return JsonResponse(data, content_type='application/json', safe=False, status= 200)
        else:
          return HttpResponse(False, content_type='application/json', status=401)
      except (User.DoesNotExist, Token.DoesNotExist):
        return HttpResponse("The user or token does not exist", content_type='application/json', status=401)
    else:
      return HttpResponse(ERROR_POST_REQUIRED, content_type='application/json', status=405)

def save_movie(request):
  if request.method == 'POST':
    imdb_id = request.POST.get('imdb_id')
    try:
      movie = Movie.objects.get(imdb_id=imdb_id)
      data = MovieSerializer(movie).data
      return JsonResponse(data, content_type='application/json', safe=False, status=409)
    except Movie.DoesNotExist:
      serializer = save_movie_in_db(imdb_id)
      if serializer.is_valid():
        return JsonResponse(serializer.data, content_type='application/json', safe=False, status=201)
      return JsonResponse(serializer.errors, status=400, content_type='application/json')
  else:
    return HttpResponse(ERROR_POST_REQUIRED, content_type='application/json', status=405)

def get_genres(request):
    if request.method == 'GET':
        genres = Genre.objects.all()
        data = CustomGenreSerializer(genres, many=True).data
        return JsonResponse(data, content_type='application/json', safe=False, status=200)
    else:
        return HttpResponse(ERROR_GET_REQUIRED, content_type='application/json', status=405)

def save_group(request):
  if request.method == 'POST':
    title = request.POST.get('title')
    if title is None:
      return HttpResponse("Title is required", content_type='application/json', status=400)
    user_id = request.POST.get('user_id')
    if user_id is None:
      return HttpResponse(ERROR_USER_REQUIRED, content_type='application/json', status=400)
    try:
      user = User.objects.get(id=user_id)
      user_groups_joined = IsPartOf.objects.filter(user=user).count()
      max_user_groups = GroupLevel.objects.get(id=user.group_level.id).number_of_groups
      if user_groups_joined >= max_user_groups:
        return HttpResponse("User has reached max number of groups", content_type='application/json', status=400)
      group = GroupList.objects.create(title=title)
      IsPartOf.objects.create(user=user, group=group, is_creator=True)
      return JsonResponse(CustomGroupListSerializer(group).data, content_type='application/json', safe=False, status=201)
    except User.DoesNotExist:
      return HttpResponse(ERROR_USER_NOT_EXIST, content_type='application/json', status=400)
  else:
    return HttpResponse(ERROR_POST_REQUIRED, content_type='application/json', status=405)

def delete_group(request):
  if request.method == 'POST':
    group_id = request.POST.get('group_id')
    if group_id is None:
      return HttpResponse(ERROR_GROUP_REQUIRED, content_type='application/json', status=400)
    user_id = request.POST.get('user_id')
    if user_id is None:
      return HttpResponse(ERROR_USER_REQUIRED, content_type='application/json', status=400)
    try:
      group = GroupList.objects.get(id=group_id)
    except GroupList.DoesNotExist:
      return HttpResponse(ERROR_GROUP_NOT_EXIST, content_type='application/json', status=404)
    try:
      user = User.objects.get(id=user_id)
    except User.DoesNotExist:
      return HttpResponse(ERROR_USER_NOT_EXIST, content_type='application/json', status=404)
    try:  
      is_part_of = IsPartOf.objects.get(group=group, user=user)
      if is_part_of.is_creator:
        group.delete()
        return HttpResponse('Group deleted', content_type='application/json', status=200)
      else:
        return HttpResponse('Only creator can delete group', content_type='application/json', status=401)
    except IsPartOf.DoesNotExist:
      return HttpResponse(ERROR_USER_NOT_IN_GROUP, content_type='application/json', status=404)
  else:
    return HttpResponse(ERROR_POST_REQUIRED, content_type='application/json', status=405)

def join_group(request):
  if request.method == 'POST':
    group_id = request.POST.get('group_id')
    if group_id is None:
      return HttpResponse(ERROR_GROUP_REQUIRED, content_type='application/json', status=400)
    user_id = request.POST.get('user_id')
    if user_id is None:
      return HttpResponse(ERROR_USER_REQUIRED, content_type='application/json', status=400)
    try:
      group = GroupList.objects.get(id=group_id)
    except GroupList.DoesNotExist:
      return HttpResponse(ERROR_GROUP_NOT_EXIST, content_type='application/json', status=404)
    try:
      user = User.objects.get(id=user_id)
      user_groups_joined = IsPartOf.objects.filter(user=user).count()
      max_user_groups = GroupLevel.objects.get(id=user.group_level.id).number_of_groups
      if user_groups_joined >= max_user_groups:
        return HttpResponse("User has reached max number of groups", content_type='application/json', status=400)
    except User.DoesNotExist:
      return HttpResponse(ERROR_USER_NOT_EXIST, content_type='application/json', status=404)
    try:
      IsPartOf.objects.get(group=group, user=user)      
      return HttpResponse('User is already part of this group', content_type='application/json', status=400)
    except IsPartOf.DoesNotExist:
      IsPartOf.objects.create(user=user, group=group)
      return HttpResponse('User joined group', content_type='application/json', status=200)
  else:
    return HttpResponse(ERROR_POST_REQUIRED, content_type='application/json', status=405)

def get_groups(request):
  if request.method == 'GET':
    user_id = request.GET.get('user_id')
    if user_id is None:
      return HttpResponse(ERROR_USER_REQUIRED, content_type='application/json', status=400)
    try:
      user = User.objects.get(id=user_id)
    except User.DoesNotExist:
      return HttpResponse(ERROR_USER_NOT_EXIST, content_type='application/json', status=404)
    groups = IsPartOf.objects.filter(user=user)
    data = []
    for group in groups:
      temp = CustomGroupListSerializer(group.group).data
      group = GroupList.objects.get(id=group.group.id)
      is_part_of = IsPartOf.objects.filter(group=group, is_creator=True)
      creator_user_id = is_part_of[0].user.id
      creator_infos = User.objects.get(id=creator_user_id)
      temp['creator_infos'] = GroupUserDetailsSerializer(creator_infos).data
      data.append(temp)
    if len(data) == 0:
      return HttpResponse('User is not part of any groups', content_type='application/json', status=404)
    return JsonResponse(data, content_type='application/json', safe=False, status=200)
  else:
    return HttpResponse(ERROR_GET_REQUIRED, content_type='application/json', status=405)

def get_group(request):
  if request.method == 'POST':
    _group_id = request.POST.get('group_id')
    if _group_id is None:
      return HttpResponse(ERROR_GROUP_REQUIRED, content_type='application/json', status=400)
    _user_id = request.POST.get('user_id')
    if _user_id is None:
      return HttpResponse(ERROR_USER_REQUIRED, content_type='application/json', status=400)
    try:
      _group = GroupList.objects.get(id=_group_id)
    except GroupList.DoesNotExist:
      return HttpResponse(ERROR_GROUP_NOT_EXIST, content_type='application/json', status=404)
    try:
      _user = User.objects.get(id=_user_id)
    except User.DoesNotExist:
      return HttpResponse(ERROR_USER_NOT_EXIST, content_type='application/json', status=404)
    try:
      _is_part_of = IsPartOf.objects.get(user=_user, group=_group)
    except IsPartOf.DoesNotExist:
      return HttpResponse(ERROR_USER_NOT_IN_GROUP, content_type='application/json', status=404)
    _data = CustomGroupListSerializer(_group).data
    _is_part_of = IsPartOf.objects.filter(group=_group, is_creator=True)
    _creator_infos = User.objects.get(id=_is_part_of[0].user.id)
    _data['creator_infos'] = GroupUserDetailsSerializer(_creator_infos).data
    _movies = HasProposed.objects.filter(partOf_id=_is_part_of[0].id)
    _movie_temp = []
    for movie in _movies:
      _movie_temp.append(MovieSerializer(movie.movie).data)
    _data['movies'] = _movie_temp
    _members = IsPartOf.objects.filter(group=_group)
    _member_temp = []
    for member in _members:
      _member_temp.append(GroupUserDetailsSerializer(member.user).data)
    _data['members'] = _member_temp
    return JsonResponse(_data, content_type='application/json', safe=False, status=200)
  else:
    return HttpResponse(ERROR_POST_REQUIRED, content_type='application/json', status=405)

def propose_movie(request):
  if request.method == 'POST':
    _comments = request.POST.get('comments')
    _group_id = request.POST.get('group_id')
    if _group_id is None:
      return HttpResponse(ERROR_GROUP_REQUIRED, content_type='application/json', status=400)
    _user_id = request.POST.get('user_id')
    if _user_id is None:
      return HttpResponse(ERROR_USER_REQUIRED, content_type='application/json', status=400)
    _movie_id = request.POST.get('movie_id')
    if _movie_id is None:
      return HttpResponse("Movie id is required", content_type='application/json', status=400)
    try:
      _group = GroupList.objects.get(id=_group_id)
    except GroupList.DoesNotExist:
      return HttpResponse(ERROR_GROUP_NOT_EXIST, content_type='application/json', status=404)
    try:
      _user = User.objects.get(id=_user_id)
    except User.DoesNotExist:
      return HttpResponse(ERROR_USER_NOT_EXIST, content_type='application/json', status=404)
    try:
      _movie = Movie.objects.get(imdb_id=_movie_id)
    except Movie.DoesNotExist:
      save_movie_in_db(_movie_id)
    _movie = Movie.objects.get(imdb_id=_movie_id)
    try:
      _is_part_of = IsPartOf.objects.get(user=_user, group=_group)
    except IsPartOf.DoesNotExist:
      return HttpResponse(ERROR_USER_NOT_IN_GROUP, content_type='application/json', status=404)
    try:
      HasProposed.objects.get(partOf_id=_is_part_of.id, movie=_movie)
      return HttpResponse('Movie is already proposed', content_type='application/json', status=400)
    except HasProposed.DoesNotExist:
      HasProposed.objects.create(partOf_id=_is_part_of.id, movie=_movie, comments=_comments)
      return HttpResponse('Movie proposed', content_type='application/json', status=200)
  else:
    return HttpResponse(ERROR_POST_REQUIRED, content_type='application/json', status=405)
      


    

