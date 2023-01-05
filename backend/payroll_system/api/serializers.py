from dataclasses import field
from rest_framework import serializers

from .models import Company, CompanyDetails, User
from rest_framework import serializers



class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields =  ('id', 'name', 'user')

        # def to_representation(self, instance):
        #     response = super().to_representation(instance)
        #     response['user'] = UserSerializer(instance.user).data
        #     print(response)
        #     return response

class CreateCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ('name',)

class CompanyEntrySerializer(serializers.ModelSerializer):
    #comp = serializers.StringRelatedField(many=False, read_only=True)
    class Meta:
        model = CompanyDetails
        #fields = ('company', 'address', 'key_person', 'involving_industry', 'phone_no', 'email', 'pf_no', 'esi_no', 'head_office_address', 'pan_no', 'tin_no', 'registration_no', 'registration_date')
        fields = ('company', 'address', 'key_person' ,'involving_industry', 'phone_no', 'email', 'pf_no', 'esi_no', 'head_office_address', 'pan_no', 'tin_no', 'registration_no', 'registration_date')

        def to_representation(self, instance):
            print(instance)
            response = super().to_representation(instance)
            response['company'] = CompanySerializer(instance.company).data
            print(response)
            return response

            # self.fields['company'] =  CompanySerializer(read_only=True)
            # return super(CompanyEntrySerializer, self).to_representation(instance)

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_active']
        read_only_field = ['is_active']
