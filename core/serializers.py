from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class HasuraTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add Hasura custom claims
        token['https://hasura.io/jwt/claims'] = {
            # Modify these based on your user roles implementation
            'x-hasura-allowed-roles': ['user', 'admin'] if user.is_superuser else ['user'],
            'x-hasura-default-role': 'admin' if user.is_superuser else 'user',
            'x-hasura-user-id': str(user.id),
            # Add any other custom claims you need
            'x-hasura-org-id': '123',  # Example - customize based on your needs
            'x-hasura-custom-claim': 'custom-value'
        }

        # Add other custom claims if needed
        token['name'] = user.username
        token['email'] = user.email

        return token
