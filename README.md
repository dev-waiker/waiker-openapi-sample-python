# Waiker Open API (Python) Samples

웨이커 오픈 API를 python 환경에서 사용하기 위한 샘플코드 레포지토리입니다.

**오픈 API들의 Request, Response 모델들은 [웨이커 API 문서](https://docs.waiker.ai/) 를 확인해주세요**

## REST API 요청 포맷
모든 웨이커 API 는 https를 통해 요청됩니다.
API를 요청하기 위해서는 인증 정보를 Header에 담아 같이 요청해야 합니다.

## 인증 정보 생성을 위한 사전 작업

[문서보기](https://docs.waiker.ai/v2.0.0/docs/%EC%9D%B8%EC%A6%9D%ED%82%A4-%EC%9A%94%EC%B2%AD%ED%95%98%EA%B8%B0)

인증 정보를 생성하기위해 사전에 [Waiker Dashboard](https://dashboard.waiker.ai/key-management)에서 생성한 
- **Product Key**
- **UserKey**
- **SecretKey**

위 세가지 정보가 필요합니다.

## 인증 헤더 정보
HTTP Header로 인증정보를 전달하며 필요한 인증 정보는 아래와 같습니다.

| Header             | value                                                        |
| ------------------ | ------------------------------------------------------------ |
| Waiker-Product-Key | 웨이커에서 발행되는 프로덕트 키                              |
| Authorization      | Bearer {웨이커에서 발행되는 유저키와 시크릿 키를 이용하여 생성한 JWT} |

## JWT 생성 방법
웨이커에서 발행되는 **User Key**를 **Secret Key**로 서명한 JWT입니다.
서명방식은 **HS256**을 사용하며, payload는 아래와 같습니다.

```
{
  "userKey" : "{userKey}"
}
```

## JWT 생성 예시 코드
```python
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
```