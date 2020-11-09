from django.urls import path
from taq.views import ViscidusPoisonTick, BossNatureProtection

urlpatterns = [
    path('/viscidus_poison_tick', ViscidusPoisonTick.as_view()),
    path('/boss_nature_protection', BossNatureProtection.as_view()),
]