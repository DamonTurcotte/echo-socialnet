from oauth2_provider.oauth2_validators import OAuth2Validator

class CustomValidator(OAuth2Validator):
    oidc_claim_scope = None

    def get_additional_claims(self, request):
        return {
            "given_name": request.user.first_name,
            "family_name": request.user.last_name,
            "email": request.user.email,
            "preferred_username": request.user.username,
            "picture": request.user.avatar,
        }