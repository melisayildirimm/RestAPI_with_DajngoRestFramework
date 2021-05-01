from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers
from .models import userInfo


class userInfoSerializer(serializers.Serializer):
    """class Meta:
        model = userInfo
        #fields = ['id', 'firstname', 'lastname', 'address', 'email', 'phone']
        fields = '__all__'
        #ordering = ['-id']"""

    id = serializers.IntegerField(read_only=True, required=False)
    firstname = serializers.CharField(max_length=50)
    lastname = serializers.CharField(max_length=50)
    address = serializers.CharField(style={'base_template': 'textarea.html'})
    email = serializers.EmailField(max_length=70)
    phone = PhoneNumberField()

    def create(self, validated_data):
        print(validated_data)
        return userInfo.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.firstname = validated_data.get('firstname', instance.firstname)
        instance.lastname = validated_data.get('lastname', instance.lastname)
        instance.address = validated_data.get('address', instance.address)
        instance.email = validated_data.get('email', instance.email)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.save()
        return instance



class EmailSerializer(serializers.Serializer):
    #id = serializers.IntegerField(read_only=True)
    email = serializers.EmailField(max_length=70)

from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers
from .models import userInfo

