# List of endpoints available

## http://localhost:8000/admin/

To access the Django admin interface, you must be logged in as superuser.
To create a superuser, you must access to the Django CLI and type the     following command and follow the instructions:

    python manage.py createsuperuser

## http://localhost:8000/api-choozen/search/

    Method : POST
    Parameters : movie-title
    Returns : JSON with basic informations about the movie.

## http://localhost:8000/api-choozen/advanced_search/

    Method : POST
    Parameters : movie-title
    Returns : JSON with all informations about the movie.

## http://localhost:8000/api-choozen-auth/

  see the documentation of dj-rest-auth [here](https://dj-rest-auth.readthedocs.io/en/latest/api_endpoints.html)

## http://localhost:8000/api-choozen/get_csrf/

    Method : GET
    Parameters : None
    Returns : HttpResponse with the CSRF token.

## http://localhost:8000/api-choozen-auth/is_authenticated/

    Method : POST
    Parameters : username, token
    Returns : if the user is authenticated, returns a JSON with all the user informations, else returns False.

## http://localhost:8000/api-choozen/get_genres/

    Method : GET
    Parameters : None
    Returns : JSON with all the genres.

## http://localhost:8000/api-choozen/save_movie/

    Method : POST
    Parameters : imdb_id
    Returns : JSON with the movie informations.
    (If the movie isn't in the database, it will be added.)

## http://localhost:8000/api-choozen/save_group/

    Method : POST
    Parameters : title, user_id
    Returns : JSON with the group informations.

## http://localhost:8000/api-choozen/delete_group/

    Method : POST
    Parameters : group_id, user_id
    Returns : HttpResponse with the status code.
    (user_id must be the owner of the group.)

## http://localhost:8000/api-choozen/join_group/

    Method : POST
    Parameters : group_id, user_id
    Returns : JSON with the group informations.

## http://localhost:8000/api-choozen/get_groups/

    Method : POST
    Parameters : user_id
    Returns : JSON with all the groups (with informations of the creator) of the user.

## http://localhost:8000/api-choozen/get_group/

    Method : POST
    Parameters : group_id, user_id
    Returns : JSON with the full group informations including the movies, users and notes.

## http://localhost:8000/api-choozen/propose_movie/

    Method : POST
    Parameters : group_id, user_id, movie_id, (optional) comments
    Returns : JSON with the group informations if success.

## http://localhost:8000/api-choozen/review_movie/

    Method : POST
    Parameters : group_id, user_id, movie_id, note
    Returns : JSON with the group informations if success.