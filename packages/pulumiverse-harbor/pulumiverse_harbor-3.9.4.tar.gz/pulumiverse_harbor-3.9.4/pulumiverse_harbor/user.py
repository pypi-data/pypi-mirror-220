# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from . import _utilities

__all__ = ['UserArgs', 'User']

@pulumi.input_type
class UserArgs:
    def __init__(__self__, *,
                 email: pulumi.Input[str],
                 full_name: pulumi.Input[str],
                 password: pulumi.Input[str],
                 username: pulumi.Input[str],
                 admin: Optional[pulumi.Input[bool]] = None,
                 comment: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a User resource.
        """
        pulumi.set(__self__, "email", email)
        pulumi.set(__self__, "full_name", full_name)
        pulumi.set(__self__, "password", password)
        pulumi.set(__self__, "username", username)
        if admin is not None:
            pulumi.set(__self__, "admin", admin)
        if comment is not None:
            pulumi.set(__self__, "comment", comment)

    @property
    @pulumi.getter
    def email(self) -> pulumi.Input[str]:
        return pulumi.get(self, "email")

    @email.setter
    def email(self, value: pulumi.Input[str]):
        pulumi.set(self, "email", value)

    @property
    @pulumi.getter(name="fullName")
    def full_name(self) -> pulumi.Input[str]:
        return pulumi.get(self, "full_name")

    @full_name.setter
    def full_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "full_name", value)

    @property
    @pulumi.getter
    def password(self) -> pulumi.Input[str]:
        return pulumi.get(self, "password")

    @password.setter
    def password(self, value: pulumi.Input[str]):
        pulumi.set(self, "password", value)

    @property
    @pulumi.getter
    def username(self) -> pulumi.Input[str]:
        return pulumi.get(self, "username")

    @username.setter
    def username(self, value: pulumi.Input[str]):
        pulumi.set(self, "username", value)

    @property
    @pulumi.getter
    def admin(self) -> Optional[pulumi.Input[bool]]:
        return pulumi.get(self, "admin")

    @admin.setter
    def admin(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "admin", value)

    @property
    @pulumi.getter
    def comment(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "comment")

    @comment.setter
    def comment(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "comment", value)


@pulumi.input_type
class _UserState:
    def __init__(__self__, *,
                 admin: Optional[pulumi.Input[bool]] = None,
                 comment: Optional[pulumi.Input[str]] = None,
                 email: Optional[pulumi.Input[str]] = None,
                 full_name: Optional[pulumi.Input[str]] = None,
                 password: Optional[pulumi.Input[str]] = None,
                 username: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering User resources.
        """
        if admin is not None:
            pulumi.set(__self__, "admin", admin)
        if comment is not None:
            pulumi.set(__self__, "comment", comment)
        if email is not None:
            pulumi.set(__self__, "email", email)
        if full_name is not None:
            pulumi.set(__self__, "full_name", full_name)
        if password is not None:
            pulumi.set(__self__, "password", password)
        if username is not None:
            pulumi.set(__self__, "username", username)

    @property
    @pulumi.getter
    def admin(self) -> Optional[pulumi.Input[bool]]:
        return pulumi.get(self, "admin")

    @admin.setter
    def admin(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "admin", value)

    @property
    @pulumi.getter
    def comment(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "comment")

    @comment.setter
    def comment(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "comment", value)

    @property
    @pulumi.getter
    def email(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "email")

    @email.setter
    def email(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "email", value)

    @property
    @pulumi.getter(name="fullName")
    def full_name(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "full_name")

    @full_name.setter
    def full_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "full_name", value)

    @property
    @pulumi.getter
    def password(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "password")

    @password.setter
    def password(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "password", value)

    @property
    @pulumi.getter
    def username(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "username")

    @username.setter
    def username(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "username", value)


class User(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 admin: Optional[pulumi.Input[bool]] = None,
                 comment: Optional[pulumi.Input[str]] = None,
                 email: Optional[pulumi.Input[str]] = None,
                 full_name: Optional[pulumi.Input[str]] = None,
                 password: Optional[pulumi.Input[str]] = None,
                 username: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        ## Example Usage

        ## Import

        An internal user harbor user can be imported using the `user id` eg, `<break><break>```sh<break> $ pulumi import harbor:index/user:User main /users/19 <break>```<break><break>`

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: UserArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        ## Example Usage

        ## Import

        An internal user harbor user can be imported using the `user id` eg, `<break><break>```sh<break> $ pulumi import harbor:index/user:User main /users/19 <break>```<break><break>`

        :param str resource_name: The name of the resource.
        :param UserArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(UserArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 admin: Optional[pulumi.Input[bool]] = None,
                 comment: Optional[pulumi.Input[str]] = None,
                 email: Optional[pulumi.Input[str]] = None,
                 full_name: Optional[pulumi.Input[str]] = None,
                 password: Optional[pulumi.Input[str]] = None,
                 username: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = UserArgs.__new__(UserArgs)

            __props__.__dict__["admin"] = admin
            __props__.__dict__["comment"] = comment
            if email is None and not opts.urn:
                raise TypeError("Missing required property 'email'")
            __props__.__dict__["email"] = email
            if full_name is None and not opts.urn:
                raise TypeError("Missing required property 'full_name'")
            __props__.__dict__["full_name"] = full_name
            if password is None and not opts.urn:
                raise TypeError("Missing required property 'password'")
            __props__.__dict__["password"] = None if password is None else pulumi.Output.secret(password)
            if username is None and not opts.urn:
                raise TypeError("Missing required property 'username'")
            __props__.__dict__["username"] = username
        secret_opts = pulumi.ResourceOptions(additional_secret_outputs=["password"])
        opts = pulumi.ResourceOptions.merge(opts, secret_opts)
        super(User, __self__).__init__(
            'harbor:index/user:User',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            admin: Optional[pulumi.Input[bool]] = None,
            comment: Optional[pulumi.Input[str]] = None,
            email: Optional[pulumi.Input[str]] = None,
            full_name: Optional[pulumi.Input[str]] = None,
            password: Optional[pulumi.Input[str]] = None,
            username: Optional[pulumi.Input[str]] = None) -> 'User':
        """
        Get an existing User resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _UserState.__new__(_UserState)

        __props__.__dict__["admin"] = admin
        __props__.__dict__["comment"] = comment
        __props__.__dict__["email"] = email
        __props__.__dict__["full_name"] = full_name
        __props__.__dict__["password"] = password
        __props__.__dict__["username"] = username
        return User(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def admin(self) -> pulumi.Output[Optional[bool]]:
        return pulumi.get(self, "admin")

    @property
    @pulumi.getter
    def comment(self) -> pulumi.Output[Optional[str]]:
        return pulumi.get(self, "comment")

    @property
    @pulumi.getter
    def email(self) -> pulumi.Output[str]:
        return pulumi.get(self, "email")

    @property
    @pulumi.getter(name="fullName")
    def full_name(self) -> pulumi.Output[str]:
        return pulumi.get(self, "full_name")

    @property
    @pulumi.getter
    def password(self) -> pulumi.Output[str]:
        return pulumi.get(self, "password")

    @property
    @pulumi.getter
    def username(self) -> pulumi.Output[str]:
        return pulumi.get(self, "username")

