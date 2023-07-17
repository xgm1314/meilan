import logging

from django.shortcuts import render
from django.conf import settings

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from QQLoginTool.QQtool import OAuthQQ

from .models import OauthQQUser
from .utlis import generic_openid
from .serializers import OauthQQSerializer

logger = logging.getLogger('django')


# Create your views here.
class QQOauthURLAPIView(APIView):
    """ 拼接QQ登录的url """

    def get(self, request):
        next = request.query_params.get('next') or '/'  # 获取前端的next作为回调用

        oauth = OAuthQQ(
            client_id=settings.QQ_CLIENT_ID,
            client_secret=settings.QQ_CLIENT_SECRET,
            redirect_uri=settings.QQ_REDIRECT_URI,
            state=next
        )

        login_url = oauth.get_qq_url()
        return Response({'login_url': login_url})


class OauthQQAPIView(APIView):
    """ 用户回调接口 """

    def get(self, request):
        """ qq用户回调 """
        code = request.query_params.get('code')

        if not code:
            return Response({'message': 'qq服务器异常，请重试'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        oauth = OAuthQQ(
            client_id=settings.QQ_CLIENT_ID,
            client_secret=settings.QQ_CLIENT_SECRET,
            redirect_uri=settings.QQ_REDIRECT_URI,
            state=next
        )

        try:
            access_token = oauth.get_access_token(code)
            openid = oauth.get_open_id(access_token)
        except Exception as e:
            logger.info(e)
            return Response({'message': 'qq服务器异常'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        try:
            oauth_qq = OauthQQUser.objects.get(openid=openid)
        except OauthQQUser.DoesNotExist:
            access_token_openid = generic_openid(openid)
            return Response({'access_token': access_token_openid})

        user = oauth_qq.user  # 获取用户信息
        # 生成token数据
        from rest_framework_jwt.settings import api_settings
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        # 生成载荷信息(payload),根据user的信息生成一个payload
        payload = jwt_payload_handler(user)
        # 根据payload和secret_key，采用HS256，生成token.
        token = jwt_encode_handler(payload)
        response = Response({
            'token': token,
            'user_id': user.id,
            'username': user.username
        })

        return response

    def post(self, request):
        """ openid绑定用户接口 """
        serializer = OauthQQSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
        else:
            return Response({'message': '绑定失败'}, status=status.HTTP_400_BAD_REQUEST)

        # 生成token数据
        from rest_framework_jwt.settings import api_settings
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        # 生成载荷信息(payload),根据user的信息生成一个payload
        payload = jwt_payload_handler(user)
        # 根据payload和secret_key，采用HS256，生成token.
        token = jwt_encode_handler(payload)

        response = Response({
            'token': token,
            'user_id': user.id,
            'username': user.username
        })

        return response
