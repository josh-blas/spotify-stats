import datetime


import json


import glob

result = []


def combiner(lof):
    for k in range(0, len(lof)):

        for f in glob.glob(lof[k]):

            with open(f, "r") as infile:
                result.append(json.load(infile))

    with open("merged_file.json", "w") as outfile:
        json.dump(result, outfile)


combiner(["StreamingHistory0.json", "StreamingHistory1.json",
          "StreamingHistory2.json", "StreamingHistory3.json", "StreamingHistory4.json"])


class File:

    def __init__(self, fname):
        '''file constructor with name and handle as attributes'''
        self.fname = fname
        self.fhand = open(self.fname)

    def set_artists(self):
        '''From file history create dictionary with artists keys and count, time, dates as values'''

        def getrid(s):
            '''turns '1235    }' into 1235 as float'''
            ind = s.find('}')
            s = s[0:ind]
            s = s.strip()
            floaty = float(s)
            return floaty

        def string_to_date(s):
            '''Turn date string to date type'''
            s = s.split(' ')
            los = s[0].split('-') + s[1].split(':')
            los2 = []
            for num in los:
                if num[0] == '0':
                    los2.append(num[1])
                else:
                    los2.append(num)
            dt = datetime.datetime(int(los2[0]), int(los2[1]), int(
                los2[2]), int(los2[3]), int(los2[4]), 0)
            return dt

        # opening file and stripping whitespace
        names = ''.join(self.fhand)    # make fhand into one long str
        names = names.split(',')  # make one long str into lot

        # make a list of the form ['"Drake"', 205426, '"Tee Grizzley"', 167704]
        lst = []
        for string in names:
            if 'artistName' in string:
                ind1 = string.find(':')
                nm1 = string[ind1 + 2:]
                nm1 = nm1.strip('"')
                lst.append(nm1)
            elif 'msPlayed' in string:
                ind2 = string.find(':')
                nm2 = string[ind2 + 2:]
                nm2 = getrid(nm2)
                lst.append(nm2)
            elif 'endTime' in string:
                ind3 = string.find(':')
                nm3 = string[ind3 + 2:]
                nm3 = nm3.strip('"')
                nm3 = string_to_date(nm3)
                count = 1
                lst.append(count)
                lst.append(nm3)

        # change list from ['"Drake"', 205426, '"Tee Grizzley"', 167704]
        #               -> [['"Drake"', 205426], ['"Tee Grizzley"', 167704]]
        lst_fin = []
        h = 0
        i = 1
        j = 2
        k = 3
        for item in lst:
            if type(item) == int:
                lst_fin.append([lst[h], [lst[i]], lst[j], lst[k]])
                h += 4
                i += 4
                j += 4
                k += 4

        # make dict with artists as keys; and counts, times and listofdates as values
        d = {}
        for item in lst_fin:
            if item[2] not in d.keys():
                d[item[2]] = [item[0], item[3], item[1]]
            elif item[2] in d.keys():
                d[item[2]] = [d[item[2]][0] + item[0], d[item[2]]
                              [1] + item[3], d[item[2]][2] + (item[1])]
        return d

    def set_tracks(self):
        '''From file history create dictionary with tracks as keys; and artist, count, time, dates as values'''
        def getrid(s):
            '''turns '1235    }' into 1235 as float'''
            ind = s.find('}')
            s = s[0:ind]
            s = s.strip()
            floaty = float(s)
            return floaty

        def string_to_date(s):
            '''Turn date string to date type'''
            s = s.split(' ')
            los = s[0].split('-') + s[1].split(':')
            los2 = []
            for num in los:
                if num[0] == '0':
                    los2.append(num[1])
                else:
                    los2.append(num)
            dt = datetime.datetime(int(los2[0]), int(los2[1]), int(
                los2[2]), int(los2[3]), int(los2[4]), 0)
            return dt

        # opening file and stripping whitespace
        names = ''.join(self.fhand)  # make fhand into one long str
        names = names.split(',')  # make one long str into lot

        # make a list of the form ['"Drake"', '"Money In The Grave (Drake ft. Rick Ross)"', 205426]
        lst = []
        for string in names:
            if 'trackName' in string:
                ind1 = string.find(':')
                nm1 = string[ind1 + 2:]
                nm1 = nm1.strip('"')
                lst.append(nm1)
            elif 'artistName' in string:
                ind2 = string.find(':')
                nm2 = string[ind2 + 2:]
                nm2 = nm2.strip('"')
                lst.append(nm2)
            elif 'msPlayed' in string:
                ind3 = string.find(':')
                nm3 = string[ind3 + 2:]
                nm3 = getrid(nm3)
                lst.append(nm3)
            elif 'endTime' in string:
                ind4 = string.find(':')
                nm4 = string[ind4 + 2:]
                count = 1
                nm4 = nm4.strip('"')
                nm4 = string_to_date(nm4)
                lst.append(count)
                lst.append(nm4)

        # change from ['"Drake"', '"Money In The Grave (Drake ft. Rick Ross)"', 205426]
        #          -> [['"Money In The Grave (Drake ft. Rick Ross)" | "Drake"', 205426]]
        lst_fin = []
        h = 0
        i = 1
        j = 2
        k = 3
        l = 4
        for item in lst:
            if type(item) == int:
                lst_fin.append([lst[h], [lst[i]], lst[j], lst[k], lst[l]])
                h += 5
                i += 5
                j += 5
                k += 5
                l += 5

        # create dictionary with tracks as keys; and artist, count, time, dates as values
        d = {}
        for item in lst_fin:
            if item[3] not in d.keys():
                d[item[3]] = [item[2], item[0], item[4], item[1]]
            elif item[3] in d.keys():
                d[item[3]] = [d[item[3]][0], d[item[3]][1] + item[0],
                              d[item[3]][2] + item[4], d[item[3]][3] + item[1]]
        return d

    def set_tracks_date(self):
        '''From file history create dictionary with tracks as keys; and artist, count, time, date as value'''
        def getrid(s):
            '''turns '1235    }' into 1235 as float'''
            ind = s.find('}')
            s = s[0:ind]
            s = s.strip()
            floaty = float(s)
            return floaty

        def string_to_date(s):
            '''Turn date string to date type'''
            s = s.split(' ')
            los = s[0].split('-') + s[1].split(':')
            los2 = []
            for num in los:
                if num[0] == '0':
                    los2.append(num[1])
                else:
                    los2.append(num)
            dt = datetime.datetime(int(los2[0]), int(los2[1]), int(
                los2[2]), int(los2[3]), int(los2[4]), 0)
            return dt

        # opening file and stripping whitespace
        names = ''.join(self.fhand)  # make fhand into one long str
        names = names.split(',')  # make one long str into lot

        # make a list of the form ['"Drake"', '"Money In The Grave (Drake ft. Rick Ross)"', 205426]
        lst = []
        for string in names:
            if 'trackName' in string:
                ind1 = string.find(':')
                nm1 = string[ind1 + 2:]
                nm1 = nm1.strip('"')
                lst.append(nm1)
            elif 'artistName' in string:
                ind2 = string.find(':')
                nm2 = string[ind2 + 2:]
                nm2 = nm2.strip('"')
                lst.append(nm2)
            elif 'msPlayed' in string:
                ind3 = string.find(':')
                nm3 = string[ind3 + 2:]
                nm3 = getrid(nm3)
                lst.append(nm3)
            elif 'endTime' in string:
                ind4 = string.find(':')
                nm4 = string[ind4 + 2:]
                nm4 = nm4.strip('"')
                nm4 = string_to_date(nm4)
                count = 1
                lst.append(count)
                lst.append(nm4)

        # change from ['"Drake"', '"Money In The Grave (Drake ft. Rick Ross)"', 205426]
        #          -> [['"Money In The Grave (Drake ft. Rick Ross)" | "Drake"', 205426]]
        lst_fin = []
        h = 0
        i = 1
        j = 2
        k = 3
        l = 4
        for item in lst:
            if type(item) == int:
                lst_fin.append([lst[h], lst[i], lst[j], lst[k], lst[l]])
                h += 5
                i += 5
                j += 5
                k += 5
                l += 5

        # create dictionary with tracks as keys; and artist, count, time, dates as values
        d = {}
        for item in lst_fin:
            d[item[3]] = [item[2], item[0], item[4], item[1]]
        return d


file1 = File('merged_file.json')  # make total history file object
file2 = File('merged_file.json')  # make total history file object
file3 = File('merged_file.json')  # make total history file object


dict_artists = file1.set_artists()  # make artist dictionary
# print(dict_artists)
dict_tracks = file2.set_tracks()   # make track dictionary
# print(dict_tracks)

dict_tracks_date = file3.set_tracks_date()   # make track dictionary with single dates
# print(dict_tracks_date)

#########################################################################################################


class Track(File):
    def __init__(self, track_name=None, artist_name=None, time_listened=0, play_count=0, dates_listened=None):
        '''construct track object with attributes'''
        self.track_name = track_name
        self.artist_name = artist_name
        self.time_listened = time_listened
        self.play_count = play_count
        self.dates_listened = dates_listened

    def __repr__(self):
        return f"({self.track_name} | {self.artist_name} | playcount = {self.play_count} | timelistened = {self.time_listened} hrs"

    def __str__(self):
        return f"{self.track_name} | {self.artist_name} |  playcount = {self.play_count} | timelistened = {self.time_listened} hrs"


class ListOfTrack(Track):
    def __init__(self):
        '''construct list of track objects'''
        self.lot = []

    def list_tracks(self, d):
        '''make list of track objects'''
        for key, value in d.items():
            if key == 'Unknown Track' or value[0] == 'Unknown Artist':
                continue
            else:
                self.lot.append(Track(track_name=key, artist_name=value[0], play_count=value[1],
                                      time_listened=round((value[2] / (3.6 * 10 ** 6)), 2), dates_listened=value[3]))

    def sort_tracks_count_alltime(self):
        '''sort list of track objects by playcount'''
        sorted_lot = sorted(self.lot, key=lambda Track: Track.play_count, reverse=True)
        rank = 1
        print('Top 100 Tracks | Play Count | All Time')
        for t in sorted_lot[: 100]:
            print(f'# {str(rank)} {t}')
            rank += 1
        print('\n')

    def sort_tracks_hrs_alltime(self):
        '''sort list of track objects by timelistened'''
        sorted_lot = sorted(self.lot, key=lambda Track: Track.time_listened, reverse=True)
        rank = 1
        print('Top 100 Tracks | Time Listened | All Time')
        for t in sorted_lot[: 100]:
            print(f'# {str(rank)} {t}')
            rank += 1
        print('\n')

    def recently_played(self):
        '''print last 100 songs played with date'''
        sorted_lot = sorted(self.lot, key=lambda Track: Track.dates_listened, reverse=True)
        print('Recently Played')
        for t in sorted_lot[: 100]:
            print(f' {t.track_name} | {t.artist_name} | {t.dates_listened}')
        print('\n')

    def sort_tracks_count_4weeks(self):
        '''sort tracks by count in last 4 weeks'''
        for Track in self.lot:
            lst2 = []
            for d in Track.dates_listened:
                tdelta = datetime.timedelta(days=28)
                if d > (datetime.datetime.today() - tdelta):
                    lst2 = lst2 + [d]
            Track.dates_listened = lst2
            Track.play_count = len(lst2)
        sorted_lot = sorted(self.lot, key=lambda Track: Track.play_count, reverse=True)
        print('Top 20 Tracks | Play Count | Last 4 Weeks')
        rank = 1
        for t in sorted_lot[: 20]:
            print(f'# {str(rank)} | {t.track_name} | {t.artist_name} | playcount: {t.play_count}')
            rank += 1
        print('\n')

    def sort_tracks_count_6months(self):
        '''sort tracks by count in last 6 months'''
        for Track in self.lot:
            lst2 = []
            for d in Track.dates_listened:
                tdelta = datetime.timedelta(days=180)
                if d > (datetime.datetime.today() - tdelta):
                    lst2 = lst2 + [d]
            Track.dates_listened = lst2
            Track.play_count = len(lst2)
        sorted_lot = sorted(self.lot, key=lambda Track: Track.play_count, reverse=True)
        print('Top 100 Tracks | Play Count | Last 6 Months')
        rank = 1
        for t in sorted_lot[: 100]:
            print(f'# {str(rank)} | {t.track_name} | {t.artist_name} | playcount: {t.play_count}')
            rank += 1
        print('\n')

    def sort_tracks_count_year(self):
        '''sort tracks by count in last year'''
        for Track in self.lot:
            lst2 = []
            for d in Track.dates_listened:
                tdelta = datetime.timedelta(days=365)
                if d > (datetime.datetime.today() - tdelta):
                    lst2 = lst2 + [d]
            Track.dates_listened = lst2
            Track.play_count = len(lst2)
        sorted_lot = sorted(self.lot, key=lambda Track: Track.play_count, reverse=True)
        print('Top 100 Tracks | Play Count | Last Year')
        rank = 1
        for t in sorted_lot[: 100]:
            print(f'# {str(rank)} | {t.track_name} | {t.artist_name} | playcount: {t.play_count}')
            rank += 1
        print('\n')

    def display_tracks(self):
        '''display tracks line by line'''
        for track in self.lot:
            print(track)

    def __repr__(self):
        return f"{self.lot}"

    def __str__(self):
        return f"{self.lot}"


class Artist(File):
    def __init__(self, artist_name, play_count=0, time_listened=0, dates_listened=None, following=False):
        '''construct artist object with attributes'''
        self.artist_name = artist_name
        self.play_count = play_count
        self.time_listened = time_listened
        self.dates_listened = dates_listened
        self.following = following

    def __repr__(self):
        return f"({self.artist_name} | playcount = {self.play_count}  timelistened: {self.time_listened} hrs)"

    def __str__(self):
        return f"{self.artist_name} | playcount: {self.play_count} | timelistened: {self.time_listened} hrs "


class ListOfArtist(Artist):
    def __init__(self):
        '''construct list of artist objects'''
        self.loa = []

    def list_artists(self, d):
        '''make list of track objects'''
        for key, value in d.items():
            if key == 'Unknown Artist':
                continue
            else:
                self.loa.append(Artist(artist_name=key, play_count=value[0],
                                       time_listened=round((value[1] / (3.6 * 10 ** 6)), 2), dates_listened=value[2]))

    def sort_artists_count_alltime(self):
        '''sort list of track objects by playcount'''
        sorted_loa = sorted(self.loa, key=lambda Artist: Artist.play_count, reverse=True)
        print('Top 100 Artists | Play Count | All Time')
        rank = 1
        for a in sorted_loa[: 100]:
            print(f'# {str(rank)} {a}')
            rank += 1
        print('\n')

    def sort_artists_hrs_alltime(self):
        '''sort list of track objects by timelistened'''
        sorted_loa = sorted(self.loa, key=lambda Artist: Artist.time_listened, reverse=True)
        print('Top 100 Artists | Time Listened | All Time')
        rank = 1
        for a in sorted_loa[: 100]:
            print(f'# {str(rank)} {a}')
            rank += 1
        print('\n')

    def sort_artists_count_4weeks(self):
        '''sort artists by count in last 4 weeks'''
        for Artist in self.loa:
            lst2 = []
            for d in Artist.dates_listened:
                tdelta = datetime.timedelta(days=28)
                if d > (datetime.datetime.today() - tdelta):
                    lst2 = lst2 + [d]
            Artist.dates_listened = lst2
            Artist.play_count = len(lst2)
        sorted_loa = sorted(self.loa, key=lambda Artist: Artist.play_count, reverse=True)
        print('Top 20 Artists | Play Count | Last 4 weeks')
        rank = 1
        for a in sorted_loa[: 20]:
            print(f'# {str(rank)} {a.artist_name} | playcount: {a.play_count}')
            rank += 1
        print('\n')

    def sort_artists_count_6months(self):
        '''sort artists by count in last 6 months'''
        for Artist in self.loa:
            lst2 = []
            for d in Artist.dates_listened:
                tdelta = datetime.timedelta(days=180)

                if d > (datetime.datetime.today() - tdelta):
                    lst2 = lst2 + [d]
            Artist.dates_listened = lst2
            Artist.play_count = len(lst2)
        sorted_loa = sorted(self.loa, key=lambda Artist: Artist.play_count, reverse=True)
        print('Top 100 Artists | Play Count | Last 6 Months')
        rank = 1
        for a in sorted_loa[: 100]:
            print(f'# {str(rank)} {a.artist_name} | playcount: {a.play_count}')
            rank += 1
        print('\n')

    def sort_artists_count_year(self):
        '''sort artists by count in last year'''
        for Artist in self.loa:
            lst2 = []
            for d in Artist.dates_listened:
                tdelta = datetime.timedelta(days=365)
                if d > (datetime.datetime.today() - tdelta):
                    lst2 = lst2 + [d]
            Artist.dates_listened = lst2
            Artist.play_count = len(lst2)
        sorted_loa = sorted(self.loa, key=lambda Artist: Artist.play_count, reverse=True)
        print('Top 100 Artists | Play Count | Last Year')
        rank = 1
        for a in sorted_loa[: 100]:
            print(f'# {str(rank)} {a.artist_name} | playcount: {a.play_count}')
            rank += 1
        print('\n')

    def display_artists(self):
        '''display tracks line by line'''
        for artist in self.loa:
            print(artist)

    def __repr__(self):
        return f"{self.loa}"

    def __str__(self):
        return f"{self.loa}"


LOA1 = ListOfArtist()
LOA2 = ListOfArtist()
LOA3 = ListOfArtist()
LOA4 = ListOfArtist()
LOA1.list_artists(dict_artists)
LOA2.list_artists(dict_artists)
LOA3.list_artists(dict_artists)
LOA4.list_artists(dict_artists)
LOA1.sort_artists_count_4weeks()
LOA2.sort_artists_count_6months()
LOA3.sort_artists_count_year()
LOA4.sort_artists_hrs_alltime()
# LOA.display_artists()
# LOA.sort_artists_count()
# LOA.sort_artists_time()


LOT1 = ListOfTrack()
LOT2 = ListOfTrack()
LOT3 = ListOfTrack()
LOT4 = ListOfTrack()
LOT1.list_tracks(dict_tracks)
LOT2.list_tracks(dict_tracks)
LOT3.list_tracks(dict_tracks)
LOT4.list_tracks(dict_tracks)
LOT1.sort_tracks_count_4weeks()
LOT2.sort_tracks_count_6months()
LOT3.sort_tracks_count_year()
LOT4.sort_tracks_hrs_alltime()
# LOT.display_tracks()


LOTD = ListOfTrack()
LOTD.list_tracks(dict_tracks_date)
LOTD.recently_played()
