from event import get_random_location

class Player:
    def __init__(self, id):
        self.id = id
        self.health = 100
        self.location = get_random_location()
        self.status = "alive"
    
    def status_update(self):
        if self.health <= 0:
            self.health = 0
            self.status = "dead"

    def run(self, target_location):
        loc_diff = target_location - self.location
        diff_is_positive = loc_diff > 0
        
        if loc_diff == 0:
            return
        
        if diff_is_positive:
            self.location += 1
        else:
            self.location -= 1
    
    def __str__(self):
        str_parts = []
        str_parts.append("player : %d" % self.id)
        str_parts.append("location : %d" % self.location)
        str_parts.append("health : %s" % self.health)
        str_parts.append("status : %s" % self.status)
        result_str = ", ".join(str_parts)
        return result_str
