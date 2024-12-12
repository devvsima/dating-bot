# from ..models.users import Users
# from utils.logging import logger
# from .users import get_user
    
# social_referal = ['GitHub', "Freelancehunt", "Kabanchik", "Twitch"]

# def new_referral(user: Users, inviter: int) -> None:
#     # if inviter == social_referal:
#     #     Users.update(is_invited=True).where(Users.id == user.id).execute()
#     inviter_user: Users = get_user(inviter)
#     if inviter_user:
#         if not user.is_invited:
#             Users.update(referral=Users.referral + 1).where(Users.id == inviter).execute()
#             Users.update(is_invited=True).where(Users.id == user.id).execute()
    