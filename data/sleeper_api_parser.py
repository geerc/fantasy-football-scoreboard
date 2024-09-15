import requests
from datetime import datetime
from utils import convert_time
from unittest import mock
import os
import debug
import json

API_URL = "https://api.sleeper.app/v1/league/"

class SleeperFantasyInfo():
    def __init__(self, league_id, user_id, week):
        self.league_id = league_id
        self.user_id = user_id
        self.week = week
        self.teams_info = self.get_teams(self.league_id)
        self.roster_id = self.get_roster_id(self.teams_info, self.user_id)
        self.matchup = self.get_matchup(
            self.roster_id, self.league_id, self.week, self.teams_info)

    def refresh_matchup(self):
        self.matchup = self.get_matchup(
            self.roster_id, self.league_id, self.week, self.teams_info)
        return self.get_points(self.matchup)

    def refresh_scores(self):
        return self.get_points(self.matchup)

    def get_all_matchups(self, league_id, week, teams):
        """
        Get all matchups for the specified week
        """
        url = '{0}{1}/matchups/{2}'.format(API_URL, league_id, week)
        all_matchups = []
        try:
            response = requests.get(url)
            matchups = response.json()

            # Loop through all matchups to collect details for each one
            for matchup in matchups:
                matchup_info = {}
                matchup_info['matchup_id'] = matchup['matchup_id']
                matchup_info['roster_id'] = matchup['roster_id']
                matchup_info['team_name'] = next(
                    (team for team in teams if team['roster_id'] == matchup['roster_id']), {}).get('name', 'Unknown')
                matchup_info['team_logo'] = next(
                    (team for team in teams if team['roster_id'] == matchup['roster_id']), {}).get('avatar',
                                                                                                   'noneLogo.png')
                all_matchups.append(matchup_info)

            return all_matchups

        except requests.exceptions.RequestException as e:
            debug.error("Error encountered, Can't reach Sleeper API in get_all_matchups", e)
            return all_matchups
        except Exception as e:
            debug.error("Uncaught error in get_all_matchups", e)
            return all_matchups

    def get_teams(self, league_id):
        debug.info('getting teams')
        users_url = '{0}{1}/users'.format(API_URL, league_id)
        rosters_url = '{0}{1}/rosters'.format(API_URL, league_id)
        user_info = []
        try:
            users = requests.get(users_url)
            users = users.json()
            self.get_avatars(users)
            for user in users:
                name = user['display_name']
                avatar = user['avatar']
                user_id = user['user_id']
                team_name = user['metadata'].get('team_name')
                user_dict = {"name": name, "id": user_id,
                             "avatar": avatar, "team": team_name}
                user_info.append(user_dict)
            rosters = requests.get(rosters_url)
            rosters = rosters.json()
            for roster in rosters:
                for user in user_info:
                    if user['id'] == roster['owner_id']:
                        user['roster_id'] = roster['roster_id']
                        user['players'] = roster['players']
                        break
            return user_info
        except requests.exceptions.RequestException:
            print("Error encountered, Can't reach Sleeper API")
            return 0
        except IndexError:
            print("something somehow ended up out of index")
            return 0

    def get_roster_id(self, teams, user_id):
        user = next((item for item in teams if item['id'] == user_id))
        return user['roster_id']

    def get_avatars(self, teams):
        debug.info('getting avatars')
        logospath = os.path.abspath(os.path.join(
            os.path.dirname(__file__), '..', 'logos'))
        if not os.path.exists(logospath):
            os.makedirs(logospath, 0o777)
        for team in teams:
            avatar = team['avatar']
            filename = os.path.join(
                logospath, '{0}.png'.format(team['display_name']))
            if not os.path.exists(filename):
                debug.info('downloading avatar for {0}'.format(
                    team['display_name']))
                av_url = 'https://sleepercdn.com/avatars/thumbs/{0}'.format(
                    avatar)
                r = requests.get(av_url, stream=True)
                with open(filename, 'wb') as fd:
                    print(filename)
                    for chunk in r.iter_content(chunk_size=128):
                        fd.write(chunk)
