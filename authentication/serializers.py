from rest_framework import serializers
from authentication.models import Staff


class RegistrationSerializer(serializers.ModelSerializer):

    confirmation = serializers.CharField(
        style={"input_type": "password"}, write_only=True)

    class Meta:
        model = Staff
        fields = ['email', 'password', 'confirmation', 'role']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password')
        confirmation = validated_data.pop('confirmation')
        user = self.Meta.model(**validated_data)
        if password != confirmation:
            raise serializers.ValidationError(
                {'password': 'Les mots de passes doivent etre identiques.'})
        elif password is not None:
            user.set_password(password)
        user.save()
        return user


class StaffSerializer(serializers.ModelSerializer):

    class Meta:
        model = Staff
        fields = ['id', 'email', 'role']
