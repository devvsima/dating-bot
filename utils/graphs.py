import matplotlib.pyplot as plt
from database.service.stats import get_users_invite
from data.config import DIR

default_photo_path = rf'{DIR}/photo/invites_per_user.png'


def get_invite_graph_path(path=default_photo_path) -> str:
    create_user_invite_graph(path)
    return path

def create_user_invite_graph(path) -> None:
    plt.style.use(['dark_background'])
    users, invites = get_users_invite()
    
    plt.bar(users, invites)
    plt.xlabel('Users')
    plt.ylabel('Number of Invites')
    plt.title('Invites per User')

    plt.savefig(path)

