# -*- coding: utf-8 -*-
# ****************************************************************
# IDE:          PyCharm
# Developed by: macercha
# Date:         16/04/23 18:17
# Project:      Zibanu - Django
# Module Name:  user
# Description:
# ****************************************************************
import smtplib
from django.apps import apps
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import ProtectedError
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from zibanu.django.auth.api import serializers
from zibanu.django.auth.lib.utils import get_user
from zibanu.django.utils import Email
from zibanu.django.utils import ErrorMessages
from zibanu.django.utils import CodeGenerator
from zibanu.django.rest_framework.exceptions import APIException
from zibanu.django.rest_framework.exceptions import ValidationError
from zibanu.django.rest_framework.decorators import permission_required
from zibanu.django.rest_framework.viewsets import ModelViewSet


class UserService(ModelViewSet):
    model = get_user_model()
    serializer_class = serializers.UserListSerializer
    request_password_template = settings.ZB_AUTH_REQUEST_PASSWORD_TEMPLATE
    change_password_template = settings.ZB_AUTH_CHANGE_PASSWORD_TEMPLATE

    def __send_mail(self, subject: str, to: list, template: str, context: dict) -> None:
        """
        Method to encapsulate send mail action
        :param subject: subject of mail
        :param to: target of mail
        :param template: template to be used at mail create
        :param context: context dict with values of vars used in mail
        :return: None
        """
        try:
            email = Email(subject=subject, to=to, context=context)
            email.set_text_template(template=template)
            email.set_html_template(template=template)
            email.send()
        except smtplib.SMTPException:
            pass

    def get_permissions(self):
        """
        Override get_permissions method to request password action
        :return: list of permissions
        """
        if self.action == "request_password":
            permission_classes = [AllowAny]
        else:
            permission_classes = self.permission_classes.copy()
        return [permission() for permission in permission_classes]

    @method_decorator(permission_required("auth.view_user"))
    def list(self, request, *args, **kwargs) -> Response:
        """
        Override method to add a permission required for list user
        :param request: HTTP request object
        :param args: args for list method
        :param kwargs: kwargs for list method
        :return: response with list
        """
        kwargs = dict({"order_by": "first_name", "is_active__exact": True})
        return super().list(request, *args, **kwargs)

    @method_decorator(permission_required(["auth.add_user", "zb_auth.add_userprofile"]))
    def create(self, request, *args, **kwargs) -> Response:
        """
        Override Method
        Rest endpoint to create user with its profile.
        :param request: request object from HTTP
        :param args: args from HTTP
        :param kwargs: kwargs dict from HTTP
        :return: response object
        """
        try:
            if request.data is not None and len(request.data) > 0:
                roles_data = request.data.pop("groups", [])
                permissions_data = request.data.pop("permissions", [])
                try:
                    transaction.set_autocommit(False)
                    serializer = serializers.UserSerializer(data=request.data)
                    if serializer.is_valid(raise_exception=True):
                        created_user = serializer.create(validated_data=serializer.validated_data)
                        if created_user is not None:
                            if len(roles_data) > 0:
                                # If user has roles to add
                                created_user.groups.set(roles_data)
                            if len(permissions_data) > 0:
                                # If user has permissions to add
                                created_user.user_permissiones.set(permissions_data)
                            data_return = self.get_serializer(created_user).data
                except ValidationError as exc:
                    transaction.rollback()
                    raise
                except Exception as exc:
                    transaction.rollback()
                    raise APIException(ErrorMessages.NOT_CONTROLLED, str(exc),
                                       status.HTTP_500_INTERNAL_SERVER_ERROR) from exc
                else:
                    transaction.commit()
                finally:
                    transaction.set_autocommit(True)
            else:
                raise ValidationError(ErrorMessages.DATA_REQUEST_NOT_FOUND, "data_request_error")
        except ValidationError as exc:
            raise APIException(exc.detail[0], http_status=status.HTTP_406_NOT_ACCEPTABLE) from exc

        return Response(status=status.HTTP_201_CREATED)

    @method_decorator(permission_required(["auth.change_user", "zb_auth.change_userprofile"]))
    def update(self, request, *args, **kwargs) -> Response:
        """
        Update a user, including groups and user permissions
        :param request: request object from HTTP
        :param args: args from HTTP
        :param kwargs: kwargs dict from HTTP
        :return: response object
        """
        try:
            if "email" in request.data:
                try:
                    try:
                        transaction.set_autocommit(False)
                        user = self.model.objects.get(email__exact=request.data.get("email"))
                        if "first_name" in request.data:
                            user.first_name = request.data.get("first_name")
                        if "last_name" in request.data:
                            user.last_name = request.data.get("last_name")
                        if "is_staff" in request.data:
                            user.is_staff = request.data.get("is_staff")
                        if "is_active" in request.data:
                            user.is_active = request.data.get("is_active")
                        if "profile" in request.data:
                            user.profile.set(request.data.get("profile"))
                        if "groups" in request.data:
                            user.groups.set(request.data.get("groups"))
                        if "permissions" in request.data:
                            user.user_permissions.set(request.data.get("permissions"))
                        user.save()
                    except ObjectDoesNotExist as exc:
                        raise APIException(msg=ErrorMessages.NOT_FOUND, error="user_not_exists",
                                           http_status=status.HTTP_406_NOT_ACCEPTABLE) from exc
                    except Exception as exc:
                        transaction.rollback()
                        raise APIException(msg=ErrorMessages.NOT_CONTROLLED, error=str(exc),
                                           http_status=status.HTTP_500_INTERNAL_SERVER_ERROR) from exc
                    else:
                        transaction.commit()
                    finally:
                        transaction.set_autocommit(True)
                except self.model.DoesNotExist as exc:
                    raise ValidationError(_("User does not exists."), "user_not_exists")
            else:
                raise ValidationError(ErrorMessages.DATA_REQUEST_NOT_FOUND, "data_request_error")
        except ValidationError as exc:
            raise APIException(msg=exc.detail[0], error=exc.detail[0].code,
                               http_status=status.HTTP_406_NOT_ACCEPTABLE) from exc
        else:
            return Response(status=status.HTTP_200_OK)

    @method_decorator(permission_required(["auth.delete_user", "zb_auth.delete_userprofile"]))
    def destroy(self, request, *args, **kwargs) -> Response:
        """
        Override method to delete user from django auth sub-system
        :param request: request object from HTTP
        :param args: args tuple
        :param kwargs: kwargs dictionary
        :return: response object
        """
        try:
            if "email" in request.data:
                request_user = get_user(request.user)
                user = self.model.objects.get(email__exact=request.data.get("email"))
                if user.email != request_user.email:
                    user.delete()
                else:
                    raise ValidationError(_("Cannot delete yourself."), "delete_user_error")
            else:
                raise ValidationError(ErrorMessages.DATA_REQUEST_NOT_FOUND, "data_request_error")
        except ObjectDoesNotExist as exc:
            raise APIException(msg=ErrorMessages.NOT_FOUND, error="user_not_exists",
                               http_status=status.HTTP_404_NOT_FOUND) from exc
        except ProtectedError as exc:
            raise APIException(msg=_("User has protected child records. Cannot delete."), error="delete_user_error",
                               http_status=status.HTTP_403_FORBIDDEN) from exc
        except ValidationError as exc:
            raise APIException(msg=exc.detail[0], error=exc.detail[0].code,
                               http_status=status.HTTP_406_NOT_ACCEPTABLE) from exc
        except Exception as exc:
            raise APIException(msg=str(exc), error="not_controlled_exception",
                               http_status=status.HTTP_500_INTERNAL_SERVER_ERROR) from exc
        else:
            return Response(status=status.HTTP_200_OK)

    def change_password(self, request, *args, **kwargs) -> Response:
        """
        REST endpoint to change password based on request user.
        :param request: request object from HTTP
        :param args: args from HTTP
        :param kwargs: kwargs from HTTP
        :return: response object
        """
        try:
            user = get_user(request.user)
            if {"old_password", "new_password"} <= request.data.keys():
                if user.check_password(request.data.get("old_password")):
                    user.set_password(request.data.get("new_password"))
                    user.save()
                    context = {
                        "user": user
                    }
                    if apps.is_installed("zibanu.django"):
                        self.__send_mail(subject=_("Password change"), to=[user.email],
                                         template=self.change_password_template, context=context)
                else:
                    raise ValidationError(_("Old password does not match."))
            else:
                raise ValidationError(_("Old/New password are required."))
        except ValidationError as exc:
            raise APIException(msg=exc.detail[0], error="validation_error",
                               http_status=status.HTTP_406_NOT_ACCEPTABLE) from exc
        except Exception as exc:
            raise APIException(error=str(exc), http_status=status.HTTP_500_INTERNAL_SERVER_ERROR) from exc
        else:
            return Response(status=status.HTTP_200_OK)

    def request_password(self, request, *args, **kwargs) -> Response:
        """
        REST endpoint to request password from system to email.
        :param request: HTTP request object
        :param args: args array
        :param kwargs: kwargs dict
        :return: response object
        """
        try:
            if "email" in request.data:
                user = get_user_model().objects.filter(email__exact=request.data.get("email")).first()
                if user is not None:
                    code_gen = CodeGenerator(action="request_password", code_length=12)
                    new_password = code_gen.get_alpha_numeric_code()
                    user.set_password(new_password)
                    user.save()
                    context = {
                        "user": user,
                        "new_password": new_password
                    }
                    if apps.is_installed("zibanu.django"):
                        self.__send_mail(subject=_("Request password."), to=[user.email],
                                         template=self.request_password_template, context=context)
                else:
                    raise ValidationError(_("Email is not registered."))
            else:
                raise ValidationError(ErrorMessages.DATA_REQUEST_NOT_FOUND)
        except ValidationError as exc:
            raise APIException(msg=exc.detail[0], error="validation_error",
                               http_status=status.HTTP_406_NOT_ACCEPTABLE) from exc
        except Exception as exc:
            raise APIException(error=str(exc), http_status=status.HTTP_500_INTERNAL_SERVER_ERROR) from exc
        else:
            return Response(status=status.HTTP_200_OK)
