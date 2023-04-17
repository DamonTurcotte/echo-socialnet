from oauth2_provider.oauth2_validators import OAuth2Validator

class CustomOAuth2Validator(OAuth2Validator):
    # "None" ignores scopes that limit claims to return, otherwise standard scopes are used.
    oidc_claim_scope = None
    def get_additional_claims(self, request):
        claims = {
            "uuid": request.user.uuid,
            "username": request.user.username,
            "avatar": request.user.avatar.url,
        }

        return claims