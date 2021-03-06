import csv
import click

def geometricSum(x,n):
    return int(round((1-pow(x,n))/(1-x)))

@click.command()
@click.option('--usersperteam', '-upt', default=5, help='Average number of users per Team')
@click.option('--resourcesperteam', '-rpt', default=5, help='Number of resources per Team')
@click.option('--hierarchies', '-h', default=10, help='Number of Team hierarchies, must be > 0')
@click.option('--childteams', '-ct', default=3, help='Number of child teams')
def create_csv(usersperteam, resourcesperteam, hierarchies, childteams):

    numberOfTeams = geometricSum(childteams, hierarchies)

    #  NODES
    # Create Team nodes file
    startIdTeam = 0
    with open('largegraph/Team.csv', 'w') as teamFile:
        fieldnames = ['teamId', 'name', 'type']
        writer = csv.DictWriter(teamFile, fieldnames=fieldnames)
        writer.writeheader()
        for x in range(0,numberOfTeams):
            writer.writerow({'teamId':x,'name':'Team ' + str(x),'type':'Team'})

    startIdUser = startIdTeam + numberOfTeams
    # Create User nodes file
    with open('largegraph/User.csv', 'w') as userFile:
        fieldnames = ['userId', 'name', 'type']
        writer = csv.DictWriter(userFile, fieldnames=fieldnames)
        writer.writeheader()
        for x in range(0,numberOfTeams*usersperteam):
            writer.writerow({'userId':x,'name':'User ' + str(x),'type':'User'})

    startIdResource = startIdUser + numberOfTeams*usersperteam
    # Create Resource node file
    with open('largegraph/Resource.csv', 'w') as resourceFile:
        fieldnames = ['resourceId', 'name', 'type']
        writer = csv.DictWriter(resourceFile, fieldnames=fieldnames)
        writer.writeheader()
        for x in range(0,numberOfTeams*resourcesperteam):
            writer.writerow({'resourceId':x,'name':'Resource ' + str(x),'type':'Resource'})

    #  RELATIONSHIPS
    with open('largegraph/PART_OF_TEAM.csv', 'w') as partOfTeamFile:
        writer = csv.writer(partOfTeamFile)
        for x in range(0,numberOfTeams*usersperteam):
            teamId = int(x / usersperteam)
            writer.writerow([startIdUser+x, teamId])

    # Team of Teams.  Team 1 is the top organisation team
    with open('largegraph/PART_OF_TEAM.csv', 'a') as teamOfTeamFile:
        writer = csv.writer(teamOfTeamFile)
        for x in range(1,hierarchies):
            for y in range(geometricSum(childteams,x),geometricSum(childteams,x+1)):
                endTeamId = geometricSum(childteams,x-1) + int((y + 1 - (geometricSum(childteams,x)+1))/childteams)
                writer.writerow([y,endTeamId])

    # Each team has acces to {resources per team}
    with open('largegraph/RESOURCE_ACCESS.csv', 'w') as resourceAccessFile:
        writer = csv.writer(resourceAccessFile)
        for x in range(0,numberOfTeams*resourcesperteam):
            teamId = int(x / resourcesperteam)
            writer.writerow([teamId, startIdResource+x])

if __name__ == '__main__':
  create_csv()
