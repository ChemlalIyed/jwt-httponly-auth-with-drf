from rest_framework.serializers import ModelSerializer
from .models import User
class UserSerializer(ModelSerializer):
    class Meta:
        model=User
        fields=["id","email","username","password"]
        extra_kwargs={
            "password":{
                "write_only":True,
                "required": True
            },
            "email":{
                "required": True
            }

        }
    def create(self, validated_data):
        password = validated_data.pop('password')
        instance = User.objects.create(**validated_data)
        instance.set_password(password)
        instance.is_active=False
        instance.save()
        return instance
           