from random import randint

MAX_LOCATION = 100

def get_random_location():
    return randint(0,MAX_LOCATION)

if __name__ == "__main__":
    for i in range(10):
        print(get_random_location())
         
def battle(player_list):
    print("battles betwwen players!")
    winner_index = randint(0, len(player_list)-1)
    for i in range(len(player_list)):
        if i == winner_index:
            player_list[i].health += 10
            print("\tplayer %d, wins" % player_list[i].id)
        else:
            player_list[i].health = 0
            print("\tplayer %d, loses" % player_list[i].id)