class MonsterClassificationAgent:
    def __init__(self):
        # If you want to do any initial processing, add it here.
        pass

    def solve(self, samples, new_monster):
        positive_samples = {
            "size": [],
            "color": [],
            "covering": [],
            "foot-type": [],
            "leg-count": [],
            "arm-count": [],
            "eye-count": [],
            "horn-count": [],
            "lays-eggs": [],
            "has-wings": [],
            "has-gills": [],
            "has-tail": [],
        }

        for i in samples:
            if i[1] is True:
                for key, value in i[0].items():
                    if key == 'has_gills':
                        key = 'has-gills'
                    this_list = positive_samples.get(key)
                    if value not in this_list:
                        this_list.append(value)

        counter = 0
        for key in new_monster:
            if key == 'has_gills':
                key = 'has-gills'
            if new_monster.get(key) in positive_samples.get(key):
                counter = counter + 1

        if counter >= 9:
            return True
        else:
            return False
