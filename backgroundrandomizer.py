import random
import time

def to_tile_index(x, y):
    return x*18 + y

def shuffle_backgrounds(stored_datas):
    #start_time = time.time()
    shuffler = BackgroundShuffler(stored_datas)
    shuffler.shuffle()
    print('Backgrounds shuffled')

    shuffler = RoomColorShuffler(stored_datas)
    shuffler.shuffle()
    print('Tile colors shuffled')
    #print('Backgrounds shuffled in %f seconds' % (time.time()-start_time))


class BackgroundShuffler(object):
    def __init__(self, stored_datas):
        self.stored_datas = stored_datas
        original_locations = []

        filter_function = self.filter_function
        for areaid, data in stored_datas.items():
            original_locations += ((areaid, posindex, val)
                for posindex, val in enumerate(data.tiledata_roombg) if filter_function(val))

        self.original_locations = original_locations

    def filter_function(self, val):
        # don't shuffle DLC backgrounds
        # don't shuffle Noah3 background because it does weird things to boss doors
        return val <= 118 and val not in (0,23,17,104,110)

    def shuffle(self):
        backgrounds = list(set(val for areaid, posindex, val in self.original_locations))
        new_backgrounds = list(backgrounds)
        random.shuffle(new_backgrounds)
        allocation = dict(zip(backgrounds, new_backgrounds))

        stored_datas = self.stored_datas
        for areaid, posindex, val in self.original_locations:
            # Fix for pyramid super-trampoline bug
            if areaid == 1 and posindex == to_tile_index(16,11): continue

            stored_datas[areaid].tiledata_roombg[posindex] = allocation[val]


class RoomColorShuffler(object):
    def __init__(self, stored_datas):
        self.stored_datas = stored_datas
        original_locations = []

        filter_function = self.filter_function
        for areaid, data in stored_datas.items():
            original_locations += ((areaid, posindex, val)
                for posindex, val in enumerate(data.tiledata_roomcolor) if filter_function(val))

        self.original_locations = original_locations

    def filter_function(self, val):
        # don't shuffle DLC colors
        # don't shuffle library color (24) because it deletes trampolines
        # don't shuffle FC2/HoM colors (6,30) because they do weird things to bosses
        return val <= 31 and val not in (0,5,6,24,30) # DLC: (0,5,32,34,55)

    def shuffle(self):
        backgrounds = list(set(val for areaid, posindex, val in self.original_locations))
        new_backgrounds = list(backgrounds)
        random.shuffle(new_backgrounds)
        allocation = dict(zip(backgrounds, new_backgrounds))

        stored_datas = self.stored_datas
        for areaid, posindex, val in self.original_locations:
            stored_datas[areaid].tiledata_roomcolor[posindex] = allocation[val]
