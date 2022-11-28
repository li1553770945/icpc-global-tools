import json
import logging
import requests

# 创建logger对象
logger = logging.getLogger('my_logger')

# 设置日志等级
logger.setLevel(logging.INFO)
# 输出的日志信息格式
formatter = logging.Formatter('%(asctime)s-%(filename)s-line:%(lineno)d-%(levelname)s: %(message)s')

# 写到控制台
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)


class People:
    def __init__(self, name, id):
        self.name = name
        self.id = id


class Team:
    def __init__(self, name, id, coach):
        self.name = name
        self.id = id
        self.members = list()
        self.coach = coach

    def add_member(self, member):
        self.members.append(member)


def get_members():
    pass


def get_teams():
    url = f"https://icpc.global/api/team/search/{CONTEST_ID}/all?q=proj:teamId,rank,site,team,country,institution,coachName,status,action%3Bsort:team+asc%3B&page=1&size=1000"
    headers = {"authorization": auth, "cookie": cookie}
    r = requests.get(url, headers=headers)
    if r.status_code != 200:
        raise ConnectionError(f"获取队伍请求失败，状态码：{r.status_code}")
    teams_origin = r.json()

    teams = list()
    for t in teams_origin:
        team = Team(t['team']['name'], t['id'], t['coach'])
        teams.append(team)
    logger.info(f"获取队伍成功，总队伍数:{len(teams)}")

    return teams


def main():
    teams = get_teams()
    print(teams[0])


if __name__ == "__main__":

    CONTEST_ID = 5544



    with open("authorization.txt") as f:
        auth = f.read()
    with open("cookie.txt") as f:
        cookie = f.read()
    main()
