from player import Player
from map import Map
from event import battle

class Game:
    def __init__(self, num_player):
        self.num_player = num_player
        self.players = []
        for player_id in range(num_player):
            self.players.append(Player(player_id))
        self.map = Map()
        self.global_time = 0

    def __str__(self):
        return "time : %d, target location : %d" % (self.global_time, self.map.target_location)

    def time_goes_by(self):
        self.global_time += 1

        for p in self.players:
            if p.status == "alive":
                p.run(self.map.target_location)    
                self.map.safe_zone_effect(p, self.global_time)
            #p_in_safe_zone = self.map.is_in_safe_zone(p.location, self.global_time)

            p.status_update()
            print(p)
            #if p_in_safe_zone:
            #   print("\t is in safe zone.")

            for i in range(len(self.players)):
                if self.players[i].status == "alive":
                    players_to_fight = [self.players[i]]
                    for j in range(len(self.players)):
                        if i == j:
                            continue
                        if self.players[i].location == self.players[j].location:
                            if self.players[j].status == "alive":
                                players_to_fight.append(self.players[j])
                    if len(players_to_fight)>1:
                        battle(players_to_fight)
                    
                    for p in players_to_fight:
                        p.status_update()
        print(self)
        print("=" * 40)

    

if __name__ == "__main__":
    g = Game(30)
    while True:
        g.time_goes_by()
        alive_players = [player for player in g.players if player.status == "alive"]
        if len(alive_players) <= 1:
            if len(alive_players) == 1:
                print("The Winner is Player " + str(alive_players[0].id))
            break
    
    #for t in range(4):
    #    g.time_goes_by()