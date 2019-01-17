from social_core.exceptions import AuthForbidden


def save_user_profile(backend, user, response, *args, **kwargs):
    print(response.keys())
    if backend.name == "google-oauth2":
        if 'gender' in response.keys():
            if response['gender'] == 'male':
                user.accountprofile.gender = 'M'
            else:
                user.accountprofile.gender = 'W'

        if 'tagline' in response.keys():
            user.accountprofile.tagline = response['tagline']

        if 'aboutMe' in response.keys():
            user.accountprofile.aboutMe = response['aboutMe']

        if 'url' in response.keys():
            user.accountprofile.url = response['url']

        if 'language' in response.keys():
            user.accountprofile.language = response['language']

        if 'ageRange' in response.keys():
            minAge = response['ageRange']['min']
            if int(minAge) < 18:
                user.delete()
                raise AuthForbidden('social_core.backends.google.GoogleOAuth2')

        user.save()

    return
