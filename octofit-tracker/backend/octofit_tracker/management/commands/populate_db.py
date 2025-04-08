from django.core.management.base import BaseCommand
from octofit_tracker.models import User, Team, Activity, Leaderboard, Workout
from django.conf import settings
from pymongo import MongoClient
from datetime import timedelta
from bson import ObjectId

class Command(BaseCommand):
    help = 'Populate the database with test data for users, teams, activity, leaderboard, and workouts'

    def handle(self, *args, **kwargs):
        # Connect to MongoDB
        client = MongoClient(settings.DATABASES['default']['HOST'], settings.DATABASES['default']['PORT'])
        db = client[settings.DATABASES['default']['NAME']]

        # Drop existing collections
        db.users.drop()
        db.teams.drop()
        db.activity.drop()
        db.leaderboard.drop()
        db.workouts.drop()

        # Create users
        users = [
            User(_id=ObjectId(), name='thundergod', email='thundergod@mhigh.edu'),
            User(_id=ObjectId(), name='metalgeek', email='metalgeek@mhigh.edu'),
            User(_id=ObjectId(), name='zerocool', email='zerocool@mhigh.edu'),
            User(_id=ObjectId(), name='crashoverride', email='crashoverride@hmhigh.edu'),
            User(_id=ObjectId(), name='sleeptoken', email='sleeptoken@mhigh.edu'),
        ]
        User.objects.bulk_create(users)

        # Create teams
        team1 = Team(_id=ObjectId(), name='Blue Team', members=[user._id for user in users[:3]])
        team2 = Team(_id=ObjectId(), name='Gold Team', members=[user._id for user in users[3:]])
        team1.save()
        team2.save()

        # Create activities
        activities = [
            Activity(_id=ObjectId(), user=users[0], type='Cycling', duration=60),
            Activity(_id=ObjectId(), user=users[1], type='Crossfit', duration=120),
            Activity(_id=ObjectId(), user=users[2], type='Running', duration=90),
            Activity(_id=ObjectId(), user=users[3], type='Strength', duration=30),
            Activity(_id=ObjectId(), user=users[4], type='Swimming', duration=75),
        ]
        Activity.objects.bulk_create(activities)

        # Create leaderboard entries
        leaderboard_entries = [
            Leaderboard(_id=ObjectId(), team=team1, score=100),
            Leaderboard(_id=ObjectId(), team=team2, score=90),
        ]
        Leaderboard.objects.bulk_create(leaderboard_entries)

        # Create workouts
        workouts = [
            Workout(_id=ObjectId(), name='Cycling Training', description='Training for a road cycling event'),
            Workout(_id=ObjectId(), name='Crossfit', description='Training for a crossfit competition'),
            Workout(_id=ObjectId(), name='Running Training', description='Training for a marathon'),
            Workout(_id=ObjectId(), name='Strength Training', description='Training for strength'),
            Workout(_id=ObjectId(), name='Swimming Training', description='Training for a swimming competition'),
        ]
        Workout.objects.bulk_create(workouts)

        self.stdout.write(self.style.SUCCESS('Successfully populated the database with test data.'))
