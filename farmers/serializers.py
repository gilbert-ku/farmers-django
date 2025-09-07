from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User, Agrovet, Farmer

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'user_type', 'must_reset_password')
        read_only_fields = ('id', 'username', 'user_type', 'must_reset_password')

class AgrovetSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Agrovet
        fields = ('id', 'user', 'business_name', 'registration_number', 'location', 'created_at')

class AgrovetRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    business_name = serializers.CharField()
    registration_number = serializers.CharField()
    location = serializers.CharField()
    
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'password', 'password2', 
                 'business_name', 'registration_number', 'location')
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError("Passwords don't match")
        return attrs
    
    def create(self, validated_data):
        # Extract agrovet-specific data
        business_name = validated_data.pop('business_name')
        registration_number = validated_data.pop('registration_number')
        location = validated_data.pop('location')
        validated_data.pop('password2')
        
        # Create user
        user = User.objects.create_user(
            username=validated_data['email'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            password=validated_data['password'],
            user_type='agrovet'
        )
        
        # Create agrovet profile
        Agrovet.objects.create(
            user=user,
            business_name=business_name,
            registration_number=registration_number,
            location=location
        )
        
        return user

class FarmerSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    registered_by = AgrovetSerializer(read_only=True)
    
    class Meta:
        model = Farmer
        fields = ('id', 'user', 'registered_by', 'farm_location', 'created_at')

class FarmerRegistrationSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField()
    farm_location = serializers.CharField()
    
    class Meta:
        model = Farmer
        fields = ('first_name', 'last_name', 'email', 'farm_location')
    
    def create(self, validated_data):
        # Generate random password
        password = self.generate_random_password()
        agrovet = self.context['request'].user.agrovet_profile
        
        # Create user
        user = User.objects.create_user(
            username=validated_data['email'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            password=password,
            user_type='farmer',
            must_reset_password=True
        )
        
        # Create farmer profile
        farmer = Farmer.objects.create(
            user=user,
            registered_by=agrovet,
            farm_location=validated_data['farm_location']
        )
        
        # Send password via email
        self.send_password_email(user, password, agrovet)
        
        return farmer
    
    def generate_random_password(self, length=12):
        characters = string.ascii_letters + string.digits + "!@#$%^&*"
        return ''.join(secrets.choice(characters) for _ in range(length))
    
    def send_password_email(self, user, password, agrovet):
        subject = 'Your Farmer Account Credentials'
        message = f"""
        Hello {user.first_name} {user.last_name},
        
        Your farmer account has been created by {agrovet.business_name}!
        
        Login Details:
        Email: {user.email}
        Temporary Password: {password}
        
        Please log in and reset your password for security.
        
        Login URL: {settings.SITE_URL}/login
        
        Best regards,
        {agrovet.business_name}
        """
        
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    
    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        
        if email and password:
            user = authenticate(username=email, password=password)
            if not user:
                raise serializers.ValidationError('Invalid credentials')
            if not user.is_active:
                raise serializers.ValidationError('User account is disabled')
            attrs['user'] = user
            return attrs
        raise serializers.ValidationError('Must include email and password')

class PasswordResetSerializer(serializers.Serializer):
    new_password = serializers.CharField(min_length=8)
    new_password2 = serializers.CharField(min_length=8)
    
    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password2']:
            raise serializers.ValidationError("Passwords don't match")
        return attrs
    
    def save(self, user):
        user.set_password(self.validated_data['new_password'])
        user.must_reset_password = False
        user.save()
        return user