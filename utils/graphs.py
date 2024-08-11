import matplotlib.pyplot as plt
from database.service.stats import get_users_invite


def create_user_invite_graph(path):
    plt.style.use(['dark_background'])
    users, invites = get_users_invite()
    
    plt.bar(users, invites)
    plt.xlabel('Users')
    plt.ylabel('Number of Invites')
    plt.title('Invites per User')

    plt.savefig(path)

