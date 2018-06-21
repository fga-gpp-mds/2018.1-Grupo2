from rest_framework import serializers
from api.models import *


class RepositorySerializer(serializers.ModelSerializer):
	class Meta:
		model = Repository
		fields = "__all__"

class ContributorSerializer(serializers.ModelSerializer):
	class Meta:
		model = Contributor
		fields = "__all__"