"""
Example usage of ClickUp SDK
"""
import asyncio
import os
from clickup_sdk import ClickUp


async def main():
    # Get token from environment variable
    token = os.getenv("CLICKUP_TOKEN", "pk_your_token_here")
    
    # Initialize ClickUp client
    async with ClickUp(token=token) as clickup:
        # Get user information
        print("Getting user information...")
        user_response = await clickup.get_user()
        user = user_response.get("user", {})
        print(f"Logged in as: {user.get('username', 'Unknown')} ({user.get('email', 'N/A')})")
        print()
        
        # Get teams (workspaces)
        print("Getting teams...")
        teams_response = await clickup.get_teams()
        teams = teams_response.get("teams", [])
        print(f"Found {len(teams)} team(s)")
        for team in teams:
            print(f"  - {team.get('name', 'Unknown')} (ID: {team.get('id')})")
        print()
        
        if teams:
            team_id = teams[0].get("id")
            
            # Get spaces
            print(f"Getting spaces for team {team_id}...")
            spaces_response = await clickup.spaces.get_spaces(team_id=team_id)
            spaces = spaces_response.get("spaces", [])
            print(f"Found {len(spaces)} space(s)")
            for space in spaces[:3]:  # Show first 3
                print(f"  - {space.get('name', 'Unknown')} (ID: {space.get('id')})")
            print()
            
            # Get time entries
            print(f"Getting time entries for team {team_id}...")
            try:
                time_entries_response = await clickup.time_entries.get_time_entries(team_id=team_id)
                time_entries = time_entries_response.get("data", [])
                print(f"Found {len(time_entries)} time entry(ies)")
            except Exception as e:
                print(f"Error getting time entries: {e}")
            print()
        
        # Example: Get a task (uncomment and provide a real task_id)
        # print("Getting task...")
        # task = await clickup.tasks.get_task("task_id_here")
        # print(f"Task: {task.get('name', 'Unknown')}")
        # print()
        
        # Example: Create a task (uncomment and provide a real list_id)
        # print("Creating task...")
        # new_task = await clickup.tasks.create_task(
        #     list_id="list_id_here",
        #     name="Test Task from SDK",
        #     description="This task was created using the ClickUp SDK",
        #     priority=2
        # )
        # print(f"Created task: {new_task.get('name', 'Unknown')}")
        # print()


if __name__ == "__main__":
    asyncio.run(main())

