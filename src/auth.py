import jwt


class JWTGenerator:
    def __init__(self, user_key=None, secret_key=None):
        self.user_key = user_key
        self.secret_key = secret_key
        self.algorithm='HS256'
        self.payload = {'userKey': f'{self.user_key}'}

    def get_auth_token(self):
        jwt_token = jwt.encode(self.payload, self.secret_key, self.algorithm)
        auth_token = f'Bearer {jwt_token}'
        return auth_token


if __name__=="__main__":
    user_key='WaikerUserKey'
    secret_key='WaikerSecretKey'
    jwt_generator = JWTGenerator(user_key=user_key, secret_key=secret_key)
    authorization_token = jwt_generator.get_auth_token()
    print(f'발급받은 User Key: {user_key}, 발급받은 Secret Key: {secret_key}')
    print(f'생성한 JWT : {authorization_token}')