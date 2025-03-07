from rest_framework import serializers
from apps.infrastructure.db.models import Consultation


class ConsultationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consultation
        fields = ['id', 'doctor', 'patient', 'created_at', 'status', 'started_at']
