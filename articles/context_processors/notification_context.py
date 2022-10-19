from articles.models import Notification


def checking_status_notification(request):
    if request.user.is_authenticated:
        status_notification = True
        notifications_user = Notification.objects \
            .filter(recipient_id=request.user.id) \
            .prefetch_related('author_id').order_by('-message_readed')
        for notification in notifications_user:
            if notification.message_readed == False:
                status_notification = False
                break

        return {'status_notification': status_notification}

    return {'status_notification': 'user_not_authenticated'}