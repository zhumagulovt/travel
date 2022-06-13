from rest_framework.routers import SimpleRouter

from .views import CommentViewSet, RatingViewSet

router = SimpleRouter()

router.register('comments', CommentViewSet)
router.register('ratings', RatingViewSet)