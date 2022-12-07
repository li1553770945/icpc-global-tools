import json
import logging

import openpyxl as openpyxl
import requests

from enum import Enum


class STATUS(Enum):
    AC = "ACCEPTED"
    CANCEL = "CANCELED"
    PENDING = "PENDING"


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

# 写到控制台
console_handler = logging.FileHandler("ac.log",encoding="utf8")
console_handler.setLevel(logging.WARNING)
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

class People:
    def __init__(self, name, id):
        self.name = name
        self.id = id


def set_status(team_id, status):
    pass


class Team:
    def __init__(self, name, id, status):
        self.name = name
        self.id = id
        self.members = list()
        self.status = status

    def add_member(self, member):
        self.members.append(member)

    def add_coaches(self, member):
        self.members.append(member)


def get_members_and_coach(id):
    url = f"https://icpc.global/api/team/members/team/{id}"
    headers = {"authorization": auth, "cookie": cookie}
    r = requests.get(url, headers=headers)
    if r.status_code != 200:
        raise ConnectionError(f"获取队伍成员，状态码：{r.status_code}")
    members = list()
    coaches = list()

    members_origin = r.json()

    for p in members_origin:
        member = People(p['name'], p['personId'])
        if p['role'] == "CONTESTANT":
            members.append(member)
        else:
            coaches.append(member)
    return members,coaches


def get_teams():
    url = f"https://icpc.global/api/team/search/{CONTEST_ID}/all?q=proj:teamId,rank,site,team,country,institution,coachName,status,action%3Bsort:team+asc%3B&page=1&size=1000"
    headers = {"authorization": auth, "cookie": cookie}
    r = requests.get(url, headers=headers)
    if r.status_code != 200:
        raise ConnectionError(f"获取队伍请求失败，状态码：{r.status_code}")
    teams_origin = r.json()

    teams = list()
    for t in teams_origin:
        team = Team(t['team']['name'], t['id'],  t['status'])
        members, coaches = get_members_and_coach(team.id)
        if len(members) == 0 or len(coaches) == 0:
            set_status(team.id, STATUS.CANCEL)  # 无队员或无教练
            logger.warning(f"队伍:\"{team.name}\",id:\"{team.id}\",无队员或无教练，取消")
            continue
        for mem in members:
            team.add_member(mem)
        for couch in coaches:
            team.add_coaches(couch)
        logger.info(f"team add success, id:\"{team.id}\",name:\"{team.name}\",members:\"{team.members[0].name}\"、\"{team.members[1].name}\"、\"{team.members[2].name}\"")
        teams.append(team)
    logger.info(f"获取队伍成功，总队伍数:{len(teams)}")

    return teams

def get_expect_teams():
    wb = openpyxl.load_workbook("icpc.xlsx")
    ws = wb.active


def main():
    teams = get_teams()
    expect_teams = get_expect_teams()

if __name__ == "__main__":
    CONTEST_ID = 5544

    with open("authorization.txt") as f:
        auth = f.read()
    with open("cookie.txt") as f:
        cookie = f.read()
    main()
