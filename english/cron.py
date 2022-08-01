from datetime import datetime
from .models import Lessons
from django_cron import CronJobBase, Schedule


class ChangeLessonsStatusJob(CronJobBase):
    schedule = Schedule(run_every_mins=1)
    code = "english.cron.ChangeLessonsStatusJob"

    def do(self):
        Lessons.objects.exclude(_status__in=[Lessons.CANCELED, Lessons.COMING_SOON]).filter(
            time_start__gt=datetime.now()
        ).update(_status=Lessons.COMING_SOON)

        Lessons.objects.exclude(_status__in=[Lessons.CANCELED, Lessons.IN_PROGRESS]).filter(
            time_start__lte=datetime.now(), time_end__gt=datetime.now()
        ).update(_status=Lessons.IN_PROGRESS)

        Lessons.objects.exclude(_status__in=[Lessons.CANCELED, Lessons.DONE]).filter(
            time_end__lte=datetime.now()
        ).update(_status=Lessons.DONE)
