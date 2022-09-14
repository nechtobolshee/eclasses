from datetime import datetime
from .models import Class, Lessons
import logging

logger = logging.getLogger('django')


class ChangeLessonsStatusJob:
    Lessons.objects.exclude(_status__in=[Lessons.CANCELED, Lessons.COMING_SOON]).filter(
        start_time__gt=datetime.now()
    ).update(_status=Lessons.COMING_SOON)

    Lessons.objects.exclude(_status__in=[Lessons.CANCELED, Lessons.IN_PROGRESS]).filter(
        start_time__lte=datetime.now(), end_time__gt=datetime.now()
    ).update(_status=Lessons.IN_PROGRESS)

    Lessons.objects.exclude(_status__in=[Lessons.CANCELED, Lessons.DONE]).filter(
        end_time__lte=datetime.now()
    ).update(_status=Lessons.DONE)


class CreateLessonsJob:
    for selected_class in Class.objects.all():
        try:
            selected_class.create_lessons()
        except:
            logger.warning(f"Failed to create lessons for {selected_class} class.")
