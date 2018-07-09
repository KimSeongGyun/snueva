from event import get_random_location

class Map:
    def __init__(self):
        self.target_location = get_random_location()
    
    def is_in_safe_zone(self, location, time):
        return abs(self.target_location - location) <= get_safe_distance(time)

    def safe_zone_effect(self, player_obj, time):
        if abs(self.target_location - player_obj.location) <= get_safe_distance(time):
            return
        else:
            player_obj.health -= 10

def get_safe_distance(time):
    if time <= 30:
        return 30
    
    if time <= 60:
        return 20
    
    if time <= 90:
        return 10
    
    if time <= 120:
        return 5
    
    if time <= 150:
        return 1