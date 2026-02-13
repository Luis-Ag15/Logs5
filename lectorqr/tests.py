from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Paciente, ScanLog

class ScanLogTest(TestCase):
    def setUp(self):
        # Create user
        self.user = User.objects.create_user(username='testuser', password='password')
        
        # Create Paciente
        self.paciente = Paciente.objects.create(
            id='ALUMNO123',
            nombre='Juan Perez',
            # Other fields can be dummy data or rely on defaults if allowed,
            # but EncryptedTextField might need value.
            # Assuming EncryptedTextField handles string input.
            edad=25,
            email='juan@example.com',
            telefono='1234567890',
            fecha_de_registro='2025-01-01',
            texto='Some text'
        )
        self.client = Client()
        self.client.login(username='testuser', password='password')

    def test_scan_log_creation(self):
        # Simulate scan
        response = self.client.post(reverse('view_detalles_paciente'), {'datoqr': 'ALUMNO123'})
        
        # Check response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['id_paciente'], 'ALUMNO123')
        
        # Check if log was created
        log = ScanLog.objects.first()
        self.assertIsNotNone(log)
        self.assertEqual(log.scanner, self.user)
        self.assertEqual(log.paciente, self.paciente)
        self.assertIsNotNone(log.timestamp)

    def test_invalid_scan_does_not_log(self):
        response = self.client.post(reverse('view_detalles_paciente'), {'datoqr': 'INVALID'})
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['id_paciente'], 0)
        
        # Should be empty if this was the only test, but depending on execution order/cleanup...
        # TestCase tears down DB between tests, so it should be empty.
        self.assertEqual(ScanLog.objects.count(), 0)
