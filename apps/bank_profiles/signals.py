# from django.dispatch import receiver
# from django.db.models.signals import post_save

# # local imports
# from .utils import generate_account_no
# from .models import Profile, AllAcountNumbers


# @receiver(post_save, sender=Profile)
# def generate_acct_number(sender, created, instance, **kwargs):
#     if created:
#         acct = generate_account_no.delay()
#         AllAcountNumbers.objects.create(user_profile=instance)
#         instance.account_no = acct
#         instance.save()


# post_save.connect(generate_acct_number, sender=Profile)
