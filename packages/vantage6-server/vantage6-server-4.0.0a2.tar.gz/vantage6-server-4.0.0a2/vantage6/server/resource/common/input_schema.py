import uuid
import ipaddress

from marshmallow import (
    Schema, fields, ValidationError, validates, validates_schema
)
from marshmallow.validate import Length, Range, OneOf

from vantage6.common.task_status import TaskStatus
from vantage6.server.default_roles import DefaultRole
from vantage6.server.model.common.utils import validate_password

_MAX_LEN_STR_SHORT = 128
_MAX_LEN_STR_LONG = 1024
_MAX_LEN_PW = 128
_MAX_LEN_NAME = 128


def _validate_name(name: str) -> None:
    """
    Validate a name field in the request input.

    Parameters
    ----------
    name : str
        Name to validate.

    Raises
    ------
    ValidationError
        If the name is empty, too long or numerical
    """
    if not len(name):
        raise ValidationError('Name cannot be empty')
    if name.isnumeric():
        raise ValidationError('Name cannot a number')
    if len(name) > _MAX_LEN_NAME:
        raise ValidationError(
            f'Name cannot be longer than {_MAX_LEN_NAME} characters'
        )


def _validate_password(password: str) -> None:
    """
    Check if the password is strong enough.

    Parameters
    ----------
    password : str
        Password to validate.

    Raises
    ------
    ValidationError
        If the password is not strong enough.
    """
    try:
        validate_password(password)
    except ValueError as e:
        raise ValidationError(str(e))


class _OnlyIdSchema(Schema):
    """ Schema for validating POST requests that only require an ID field. """
    id = fields.Integer(required=True, validate=Range(min=1))


class _NameValidationSchema(Schema):
    """ Schema for validating POST requests with a name field. """
    name = fields.String(required=True)

    @validates('name')
    def validate_name(self, name: str):
        """
        Validate the name in the input.

        Parameters
        ----------
        name : str
            Name to validate.

        Raises
        ------
        ValidationError
            If the name is empty, too long or numerical
        """
        _validate_name(name)


class _PasswordValidationSchema(Schema):
    """ Schema that contains password validation function """
    password = fields.String(required=True)

    @validates('password')
    def _validate_password(self, password: str):
        """
        Check if the password is strong enough.

        Parameters
        ----------
        password : str
            Password to validate.

        Raises
        ------
        ValidationError
            If the password is not strong enough.
        """
        _validate_password(password)


class ChangePasswordInputSchema(Schema):
    """ Schema for validating input for changing a password. """
    # validation for current password is not necessary, as it is checked in the
    # authentication process
    current_password = fields.String(required=True,
                                     validate=Length(max=_MAX_LEN_PW))
    new_password = fields.String(required=True)

    @validates('new_password')
    def validate_password(self, password: str):
        """
        Check if the password is strong enough.

        Parameters
        ----------
        password : str
            Password to validate.

        Raises
        ------
        ValidationError
            If the password is not strong enough.
        """
        _validate_password(password)


class CollaborationInputSchema(_NameValidationSchema):
    """ Schema for validating input for a creating a collaboration. """
    organization_ids = fields.List(fields.Integer(), required=True)
    encrypted = fields.Boolean(required=True)

    @validates('organization_ids')
    def validate_organization_ids(self, organization_ids):
        """
        Validate the organization ids in the input.

        Parameters
        ----------
        organization_ids : list[int]
            List of organization ids to validate.

        Raises
        ------
        ValidationError
            If the organization ids are not valid.
        """
        if not all(i > 0 for i in organization_ids):
            raise ValidationError('Organization ids must be greater than 0')
        if not len(organization_ids) == len(set(organization_ids)):
            raise ValidationError('Organization ids must be unique')
        if not len(organization_ids):
            raise ValidationError('At least one organization id is required')


class CollaborationAddOrganizationSchema(_OnlyIdSchema):
    """
    Schema for validating requests that add an organization to a collaboration.
    """
    pass


class CollaborationAddNodeSchema(_OnlyIdSchema):
    """ Schema for validating requests that add a node to a collaboration. """
    pass


class KillTaskInputSchema(_OnlyIdSchema):
    """ Schema for validating input for killing a task. """
    pass


class KillNodeTasksInputSchema(_OnlyIdSchema):
    """ Schema for validating input for killing tasks on a node. """
    pass


class NodeInputSchema(_NameValidationSchema):
    """ Schema for validating input for a creating a node. """
    # overwrite name attr as it is not required for a node
    name = fields.String(required=False)
    collaboration_id = fields.Integer(required=True, validate=Range(min=1))
    organization_id = fields.Integer(validate=Range(min=1))
    ip = fields.String()
    clear_ip = fields.Boolean()

    @validates('ip')
    def validate_ip(self, ip: str):
        """
        Validate IP address in request body.

        Parameters
        ----------
        ip : str
            IP address to validate.

        Raises
        ------
        ValidationError
            If the IP address is not valid.
        """
        try:
            ipaddress.ip_address(ip)
        except ValueError:
            raise ValidationError('IP address is not valid')


class OrganizationInputSchema(_NameValidationSchema):
    """ Schema for validating input for a creating an organization. """
    address1 = fields.String(validate=Length(max=_MAX_LEN_STR_SHORT))
    address2 = fields.String(validate=Length(max=_MAX_LEN_STR_SHORT))
    zipcode = fields.String(validate=Length(max=_MAX_LEN_STR_SHORT))
    country = fields.String(validate=Length(max=_MAX_LEN_STR_SHORT))
    domain = fields.String(validate=Length(max=_MAX_LEN_STR_SHORT))
    public_key = fields.String()


class PortInputSchema(Schema):
    """ Schema for validating input for a creating a port. """
    port = fields.Integer(required=True)
    run_id = fields.Integer(required=True, validate=Range(min=1))
    label = fields.String(validate=Length(max=_MAX_LEN_STR_SHORT))

    @validates('port')
    def validate_port(self, port):
        """
        Validate the port in the input.

        Parameters
        ----------
        port : int
            Port to validate.

        Raises
        ------
        ValidationError
            If the port is not valid.
        """
        if not 1 <= port <= 65535:
            raise ValidationError('Port must be between 1 and 65535')


class RecoverPasswordInputSchema(Schema):
    """ Schema for validating input for recovering a password. """
    email = fields.Email()
    username = fields.String(validate=Length(max=_MAX_LEN_NAME))

    @validates_schema
    def validate_email_or_username(self, data, **kwargs):
        if not ('email' in data or 'username' in data):
            raise ValidationError('Email or username is required')


class ResetPasswordInputSchema(_PasswordValidationSchema):
    """ Schema for validating input for resetting a password. """
    reset_token = fields.String(required=True,
                                validate=Length(max=_MAX_LEN_STR_LONG))


class Recover2FAInputSchema(_PasswordValidationSchema):
    """ Schema for validating input for recovering 2FA. """
    email = fields.Email()
    username = fields.String(validate=Length(max=_MAX_LEN_NAME))

    @validates_schema
    def validate_email_or_username(self, data: dict, **kwargs):
        """
        Validate the input, which should contain either an email or username.

        Parameters
        ----------
        data : dict
            The input data.

        Raises
        ------
        ValidationError
            If the input does not contain an email or username.
        """
        if not ('email' in data or 'username' in data):
            raise ValidationError('Email or username is required')


class Reset2FAInputSchema(Schema):
    """ Schema for validating input for resetting 2FA. """
    reset_token = fields.String(required=True,
                                validate=Length(max=_MAX_LEN_STR_LONG))


class ResetAPIKeyInputSchema(_OnlyIdSchema):
    """ Schema for validating input for resetting an API key. """
    pass


class RoleInputSchema(_NameValidationSchema):
    """ Schema for validating input for creating a role. """
    description = fields.String(validate=Length(max=_MAX_LEN_STR_LONG))
    rules = fields.List(fields.Integer(validate=Range(min=1)), required=True)
    organization_id = fields.Integer(validate=Range(min=1))

    @validates('name')
    def validate_name(self, name: str):
        """
        Validate that role name is not one of the default roles.

        Parameters
        ----------
        name : str
            Role name to validate.

        Raises
        ------
        ValidationError
            If the role name is one of the default roles.
        """
        if name in [role for role in DefaultRole]:
            raise ValidationError(
                'Role name cannot be one of the default roles'
            )


class RunInputSchema(Schema):
    """ Schema for validating input for patching an algorithm run. """
    started_at = fields.DateTime()
    finished_at = fields.DateTime()
    log = fields.String()
    result = fields.String()
    status = fields.String(validate=OneOf([s.value for s in TaskStatus]))


class TaskInputSchema(_NameValidationSchema):
    """ Schema for validating input for creating a task. """
    # overwrite name attr as it is not required for a task
    name = fields.String(required=False)
    description = fields.String(validate=Length(max=_MAX_LEN_STR_LONG))
    image = fields.String(required=True, validate=Length(min=1))
    collaboration_id = fields.Integer(required=True, validate=Range(min=1))
    organizations = fields.List(fields.Dict(), required=True)
    databases = fields.List(fields.String())

    @validates('organizations')
    def validate_organizations(self, organizations: list[dict]):
        """
        Validate the organizations in the input.

        Parameters
        ----------
        organizations : list[dict]
            List of organizations to validate. Each organization must have at
            least an organization id.

        Raises
        ------
        ValidationError
            If the organizations are not valid.
        """
        if not len(organizations):
            raise ValidationError('At least one organization is required')
        for organization in organizations:
            if 'id' not in organization:
                raise ValidationError(
                    'Organization id is required for each organization')


class TokenUserInputSchema(Schema):
    """ Schema for validating input for creating a token for a user. """
    username = fields.String(required=True, validate=Length(
        min=1, max=_MAX_LEN_NAME))
    # Note that we don't inherit from _PasswordValidationSchema here and
    # don't validate password in case the password does not fulfill the
    # password policy. This is e.g. the case with the default root user created
    # when the server is started for the first time.
    password = fields.String(required=True, validate=Length(
        min=1, max=_MAX_LEN_PW))
    mfa_code = fields.String(validate=Length(max=10))


class TokenNodeInputSchema(Schema):
    """ Schema for validating input for creating a token for a node. """
    api_key = fields.String(required=True)

    @validates('api_key')
    def validate_api_key(self, api_key: str):
        """
        Validate the API key in the input. The API key should be a valid UUID

        Parameters
        ----------
        api_key : str
            API key to validate.

        Raises
        ------
        ValidationError
            If the API key is not valid.
        """
        try:
            uuid.UUID(api_key)
        except ValueError:
            raise ValidationError('API key is not a valid UUID')


class TokenAlgorithmInputSchema(Schema):
    """ Schema for validating input for creating a token for an algorithm. """
    task_id = fields.Integer(required=True, validate=Range(min=1))
    image = fields.String(required=True, validate=Length(min=1))


class UserInputSchema(_PasswordValidationSchema):
    """ Schema for validating input for creating a user. """
    username = fields.String(required=True, validate=Length(
        min=1, max=_MAX_LEN_NAME
    ))
    email = fields.Email(required=True)
    firstname = fields.String(validate=Length(max=_MAX_LEN_STR_SHORT))
    lastname = fields.String(validate=Length(max=_MAX_LEN_STR_SHORT))
    organization_id = fields.Integer(validate=Range(min=1))
    roles = fields.List(fields.Integer(validate=Range(min=1)))
    rules = fields.List(fields.Integer(validate=Range(min=1)))

    @validates('username')
    def validate_username(self, username: str):
        """
        Check if the username is appropriate

        Parameters
        ----------
        username : str
            Username to validate.

        Raises
        ------
        ValidationError
            If the username is too short, too long or numeric.
        """
        _validate_name(username)


class VPNConfigUpdateInputSchema(Schema):
    """ Schema for validating input for updating a VPN configuration. """
    vpn_config = fields.String(required=True)
