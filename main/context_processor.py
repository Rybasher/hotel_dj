from .models import SocialMedia


def socials(request):
    social_medias = SocialMedia.objects.all()
    return locals()
