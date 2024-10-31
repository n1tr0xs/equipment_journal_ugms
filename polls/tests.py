from django.test import TestCase

from .models import TechnicalCondition, ServiceHistory
from .models import Peripheral

# Create your tests here.


class ServiceHistoryTest(TestCase):
    def test_peripheral_service_history(self):
        print('--- TEST Peripheral ServiceHistory ---')
        p = Peripheral.objects.create(
            name='Периферия №1',
            technical_condition=TechnicalCondition.IN_WORK
        )
        ServiceHistory.objects.create(
            device_type='периферия',
            device_id=p.id,
            description='Тестовое обслуживание №1'
        )

        history = ServiceHistory.objects.all()
        print(f'{history = }')

        p_history = p.get_service_history()
        print(f'{p_history = }')
