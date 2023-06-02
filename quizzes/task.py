from django.utils import timezone
from quizzes.models import Quiz


def update_status():
    """
    Update the status of quizzes based on their status, start datetime and end datetime.
    """
    
    now = timezone.now()
    
    # Update the status of quizzes that need their status updated
    Quiz.objects.filter(
        start_date__lte=now,
        end_date__gte=now,
    ).exclude(status=Quiz.StatusEnum.ACTIVE.value).update(
        status=Quiz.StatusEnum.ACTIVE.value
    )
    
    # Update the status of finished quizzes
    Quiz.objects.filter(
        end_date__lt=now,
        status__in=[Quiz.StatusEnum.ACTIVE.value, Quiz.StatusEnum.INACTIVE.value]
    ).update(
        status=Quiz.StatusEnum.FINISHED.value
    )
    