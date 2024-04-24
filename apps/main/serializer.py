import json
from hachoir.parser import createParser
from hachoir.metadata import extractMetadata
from rest_framework import serializers
from .models import CustomUser, FileUpload
from datetime import date
import hashlib


def file_size_validator(value):
    if value.size > 20 * 1024 * 1024:  # 20MB
        raise serializers.ValidationError("File size should not exceed 20 MB.")


class UserFileUploadSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        queryset=CustomUser.objects.all(), slug_field="mobile_number"
    )

    class Meta:
        model = FileUpload
        fields = ["user", "file", "upload_date", "metadata"]

    def validate(self, attrs):
        file = attrs.get("file")
        file_size_validator(file)
        parser = createParser(file)
        metadata = extractMetadata(parser)

        metadata_dict = {}
        for line in metadata.exportPlaintext():
            key, value = line.split(":", 1)
            metadata_dict[key.strip()] = value.strip()

        attrs["metadata"] = metadata_dict
        metadata_json = json.dumps(metadata_dict, indent=4)

        return attrs

class DateSerializer(serializers.DateField):
    def to_representation(self, value):
        return date.strftime(value, '%Y-%m-%d')

class CustomUserSerializer(serializers.ModelSerializer):
    files = serializers.SerializerMethodField()
    register_data = DateSerializer(read_only=True)

    class Meta:
        model = CustomUser
        fields = [
            "mobile_number",
            "email",
            "name",
            "family",
            "gender",
            "is_active",
            "is_admin",
            "is_superuser",
            "active_code",
            "register_data",
            "files",
            "password", 
        ]
        extra_kwargs = {'password': {'write_only': True}}  

    def get_files(self, obj):
        files = FileUpload.objects.filter(user=obj)
        serializer = UserFileUploadSerializer(files, many=True)
        return serializer.data

    def create(self, validated_data):
        password = validated_data.pop('password')
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        user = CustomUser.objects.create(**validated_data)
        user.set_password(hashed_password)
        user.save()
        return user