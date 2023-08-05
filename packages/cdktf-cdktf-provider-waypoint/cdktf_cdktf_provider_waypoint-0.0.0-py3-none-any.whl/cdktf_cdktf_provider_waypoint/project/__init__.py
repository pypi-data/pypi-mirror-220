'''
# `waypoint_project`

Refer to the Terraform Registory for docs: [`waypoint_project`](https://registry.terraform.io/providers/hashicorp/waypoint/0.1.0/docs/resources/project).
'''
import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from typeguard import check_type

from .._jsii import *

import cdktf as _cdktf_9a9027ec
import constructs as _constructs_77d1e7e8


class Project(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-waypoint.project.Project",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/waypoint/0.1.0/docs/resources/project waypoint_project}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        data_source_git: typing.Union["ProjectDataSourceGit", typing.Dict[builtins.str, typing.Any]],
        project_name: builtins.str,
        app_status_poll_seconds: typing.Optional[jsii.Number] = None,
        git_auth_basic: typing.Optional[typing.Union["ProjectGitAuthBasic", typing.Dict[builtins.str, typing.Any]]] = None,
        git_auth_ssh: typing.Optional[typing.Union["ProjectGitAuthSsh", typing.Dict[builtins.str, typing.Any]]] = None,
        project_variables: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ProjectProjectVariables", typing.Dict[builtins.str, typing.Any]]]]] = None,
        remote_runners_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/waypoint/0.1.0/docs/resources/project waypoint_project} Resource.

        :param scope: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param data_source_git: Configuration of Git repository where waypoint.hcl file is stored. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/waypoint/0.1.0/docs/resources/project#data_source_git Project#data_source_git}
        :param project_name: The name of the Waypoint project. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/waypoint/0.1.0/docs/resources/project#project_name Project#project_name}
        :param app_status_poll_seconds: Application status poll interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/waypoint/0.1.0/docs/resources/project#app_status_poll_seconds Project#app_status_poll_seconds}
        :param git_auth_basic: Basic authentication details for Git consisting of ``username`` and ``password``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/waypoint/0.1.0/docs/resources/project#git_auth_basic Project#git_auth_basic}
        :param git_auth_ssh: SSH authentication details for Git. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/waypoint/0.1.0/docs/resources/project#git_auth_ssh Project#git_auth_ssh}
        :param project_variables: List of variables in Key/value pairs associated with the Waypoint Project. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/waypoint/0.1.0/docs/resources/project#project_variables Project#project_variables}
        :param remote_runners_enabled: Enable remote runners for project. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/waypoint/0.1.0/docs/resources/project#remote_runners_enabled Project#remote_runners_enabled}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb9746c0aa81d9d3480a2fa32af683247b737ead912768d1626c69fac220b8a7)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        config = ProjectConfig(
            data_source_git=data_source_git,
            project_name=project_name,
            app_status_poll_seconds=app_status_poll_seconds,
            git_auth_basic=git_auth_basic,
            git_auth_ssh=git_auth_ssh,
            project_variables=project_variables,
            remote_runners_enabled=remote_runners_enabled,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id, config])

    @jsii.member(jsii_name="putDataSourceGit")
    def put_data_source_git(
        self,
        *,
        file_change_signal: typing.Optional[builtins.str] = None,
        git_path: typing.Optional[builtins.str] = None,
        git_poll_interval_seconds: typing.Optional[jsii.Number] = None,
        git_ref: typing.Optional[builtins.str] = None,
        git_url: typing.Optional[builtins.str] = None,
        ignore_changes_outside_path: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param file_change_signal: Indicates signal to be sent to any applications when their config files change. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/waypoint/0.1.0/docs/resources/project#file_change_signal Project#file_change_signal}
        :param git_path: Path in git repository when waypoint.hcl file is stored in a sub-directory. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/waypoint/0.1.0/docs/resources/project#git_path Project#git_path}
        :param git_poll_interval_seconds: Interval at which Waypoint should poll git repository for changes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/waypoint/0.1.0/docs/resources/project#git_poll_interval_seconds Project#git_poll_interval_seconds}
        :param git_ref: Git repository ref containing waypoint.hcl file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/waypoint/0.1.0/docs/resources/project#git_ref Project#git_ref}
        :param git_url: Url of git repository storing the waypoint.hcl file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/waypoint/0.1.0/docs/resources/project#git_url Project#git_url}
        :param ignore_changes_outside_path: Whether Waypoint ignores changes outside path storing waypoint.hcl file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/waypoint/0.1.0/docs/resources/project#ignore_changes_outside_path Project#ignore_changes_outside_path}
        '''
        value = ProjectDataSourceGit(
            file_change_signal=file_change_signal,
            git_path=git_path,
            git_poll_interval_seconds=git_poll_interval_seconds,
            git_ref=git_ref,
            git_url=git_url,
            ignore_changes_outside_path=ignore_changes_outside_path,
        )

        return typing.cast(None, jsii.invoke(self, "putDataSourceGit", [value]))

    @jsii.member(jsii_name="putGitAuthBasic")
    def put_git_auth_basic(
        self,
        *,
        password: builtins.str,
        username: builtins.str,
    ) -> None:
        '''
        :param password: Git password. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/waypoint/0.1.0/docs/resources/project#password Project#password}
        :param username: Git username. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/waypoint/0.1.0/docs/resources/project#username Project#username}
        '''
        value = ProjectGitAuthBasic(password=password, username=username)

        return typing.cast(None, jsii.invoke(self, "putGitAuthBasic", [value]))

    @jsii.member(jsii_name="putGitAuthSsh")
    def put_git_auth_ssh(
        self,
        *,
        ssh_private_key: builtins.str,
        git_user: typing.Optional[builtins.str] = None,
        passphrase: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param ssh_private_key: Private key to authenticate to Git. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/waypoint/0.1.0/docs/resources/project#ssh_private_key Project#ssh_private_key}
        :param git_user: Git user associated with private key. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/waypoint/0.1.0/docs/resources/project#git_user Project#git_user}
        :param passphrase: Passphrase to use with private key. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/waypoint/0.1.0/docs/resources/project#passphrase Project#passphrase}
        '''
        value = ProjectGitAuthSsh(
            ssh_private_key=ssh_private_key, git_user=git_user, passphrase=passphrase
        )

        return typing.cast(None, jsii.invoke(self, "putGitAuthSsh", [value]))

    @jsii.member(jsii_name="putProjectVariables")
    def put_project_variables(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ProjectProjectVariables", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eac4a7f77e3f693bbe518a0736f5b7fe6127b8f3f5a9c4591e229b75ba49cdb8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putProjectVariables", [value]))

    @jsii.member(jsii_name="resetAppStatusPollSeconds")
    def reset_app_status_poll_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAppStatusPollSeconds", []))

    @jsii.member(jsii_name="resetGitAuthBasic")
    def reset_git_auth_basic(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGitAuthBasic", []))

    @jsii.member(jsii_name="resetGitAuthSsh")
    def reset_git_auth_ssh(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGitAuthSsh", []))

    @jsii.member(jsii_name="resetProjectVariables")
    def reset_project_variables(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProjectVariables", []))

    @jsii.member(jsii_name="resetRemoteRunnersEnabled")
    def reset_remote_runners_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRemoteRunnersEnabled", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="dataSourceGit")
    def data_source_git(self) -> "ProjectDataSourceGitOutputReference":
        return typing.cast("ProjectDataSourceGitOutputReference", jsii.get(self, "dataSourceGit"))

    @builtins.property
    @jsii.member(jsii_name="gitAuthBasic")
    def git_auth_basic(self) -> "ProjectGitAuthBasicOutputReference":
        return typing.cast("ProjectGitAuthBasicOutputReference", jsii.get(self, "gitAuthBasic"))

    @builtins.property
    @jsii.member(jsii_name="gitAuthSsh")
    def git_auth_ssh(self) -> "ProjectGitAuthSshOutputReference":
        return typing.cast("ProjectGitAuthSshOutputReference", jsii.get(self, "gitAuthSsh"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="projectVariables")
    def project_variables(self) -> "ProjectProjectVariablesList":
        return typing.cast("ProjectProjectVariablesList", jsii.get(self, "projectVariables"))

    @builtins.property
    @jsii.member(jsii_name="appStatusPollSecondsInput")
    def app_status_poll_seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "appStatusPollSecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="dataSourceGitInput")
    def data_source_git_input(
        self,
    ) -> typing.Optional[typing.Union["ProjectDataSourceGit", _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union["ProjectDataSourceGit", _cdktf_9a9027ec.IResolvable]], jsii.get(self, "dataSourceGitInput"))

    @builtins.property
    @jsii.member(jsii_name="gitAuthBasicInput")
    def git_auth_basic_input(
        self,
    ) -> typing.Optional[typing.Union["ProjectGitAuthBasic", _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union["ProjectGitAuthBasic", _cdktf_9a9027ec.IResolvable]], jsii.get(self, "gitAuthBasicInput"))

    @builtins.property
    @jsii.member(jsii_name="gitAuthSshInput")
    def git_auth_ssh_input(
        self,
    ) -> typing.Optional[typing.Union["ProjectGitAuthSsh", _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union["ProjectGitAuthSsh", _cdktf_9a9027ec.IResolvable]], jsii.get(self, "gitAuthSshInput"))

    @builtins.property
    @jsii.member(jsii_name="projectNameInput")
    def project_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectNameInput"))

    @builtins.property
    @jsii.member(jsii_name="projectVariablesInput")
    def project_variables_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ProjectProjectVariables"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ProjectProjectVariables"]]], jsii.get(self, "projectVariablesInput"))

    @builtins.property
    @jsii.member(jsii_name="remoteRunnersEnabledInput")
    def remote_runners_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "remoteRunnersEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="appStatusPollSeconds")
    def app_status_poll_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "appStatusPollSeconds"))

    @app_status_poll_seconds.setter
    def app_status_poll_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__125d3794b58343c1eae21755088dff39db9e7c5d667f4d91ef8be1433850b484)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "appStatusPollSeconds", value)

    @builtins.property
    @jsii.member(jsii_name="projectName")
    def project_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "projectName"))

    @project_name.setter
    def project_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14c5e0c5be3f3d8c70bcfc75df9cc09e59376281b18b0773815a6e23e775da1a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "projectName", value)

    @builtins.property
    @jsii.member(jsii_name="remoteRunnersEnabled")
    def remote_runners_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "remoteRunnersEnabled"))

    @remote_runners_enabled.setter
    def remote_runners_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8a2c85809413f806769509b6ac4dbe415635431063b17849bf3877fa51ed3c0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "remoteRunnersEnabled", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-waypoint.project.ProjectConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "data_source_git": "dataSourceGit",
        "project_name": "projectName",
        "app_status_poll_seconds": "appStatusPollSeconds",
        "git_auth_basic": "gitAuthBasic",
        "git_auth_ssh": "gitAuthSsh",
        "project_variables": "projectVariables",
        "remote_runners_enabled": "remoteRunnersEnabled",
    },
)
class ProjectConfig(_cdktf_9a9027ec.TerraformMetaArguments):
    def __init__(
        self,
        *,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
        data_source_git: typing.Union["ProjectDataSourceGit", typing.Dict[builtins.str, typing.Any]],
        project_name: builtins.str,
        app_status_poll_seconds: typing.Optional[jsii.Number] = None,
        git_auth_basic: typing.Optional[typing.Union["ProjectGitAuthBasic", typing.Dict[builtins.str, typing.Any]]] = None,
        git_auth_ssh: typing.Optional[typing.Union["ProjectGitAuthSsh", typing.Dict[builtins.str, typing.Any]]] = None,
        project_variables: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ProjectProjectVariables", typing.Dict[builtins.str, typing.Any]]]]] = None,
        remote_runners_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param data_source_git: Configuration of Git repository where waypoint.hcl file is stored. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/waypoint/0.1.0/docs/resources/project#data_source_git Project#data_source_git}
        :param project_name: The name of the Waypoint project. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/waypoint/0.1.0/docs/resources/project#project_name Project#project_name}
        :param app_status_poll_seconds: Application status poll interval in seconds. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/waypoint/0.1.0/docs/resources/project#app_status_poll_seconds Project#app_status_poll_seconds}
        :param git_auth_basic: Basic authentication details for Git consisting of ``username`` and ``password``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/waypoint/0.1.0/docs/resources/project#git_auth_basic Project#git_auth_basic}
        :param git_auth_ssh: SSH authentication details for Git. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/waypoint/0.1.0/docs/resources/project#git_auth_ssh Project#git_auth_ssh}
        :param project_variables: List of variables in Key/value pairs associated with the Waypoint Project. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/waypoint/0.1.0/docs/resources/project#project_variables Project#project_variables}
        :param remote_runners_enabled: Enable remote runners for project. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/waypoint/0.1.0/docs/resources/project#remote_runners_enabled Project#remote_runners_enabled}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(data_source_git, dict):
            data_source_git = ProjectDataSourceGit(**data_source_git)
        if isinstance(git_auth_basic, dict):
            git_auth_basic = ProjectGitAuthBasic(**git_auth_basic)
        if isinstance(git_auth_ssh, dict):
            git_auth_ssh = ProjectGitAuthSsh(**git_auth_ssh)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3fb662a4b6582b2cd24299d38f0e68455d5bd6fbea6b15350775e5fcf482b60b)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument data_source_git", value=data_source_git, expected_type=type_hints["data_source_git"])
            check_type(argname="argument project_name", value=project_name, expected_type=type_hints["project_name"])
            check_type(argname="argument app_status_poll_seconds", value=app_status_poll_seconds, expected_type=type_hints["app_status_poll_seconds"])
            check_type(argname="argument git_auth_basic", value=git_auth_basic, expected_type=type_hints["git_auth_basic"])
            check_type(argname="argument git_auth_ssh", value=git_auth_ssh, expected_type=type_hints["git_auth_ssh"])
            check_type(argname="argument project_variables", value=project_variables, expected_type=type_hints["project_variables"])
            check_type(argname="argument remote_runners_enabled", value=remote_runners_enabled, expected_type=type_hints["remote_runners_enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "data_source_git": data_source_git,
            "project_name": project_name,
        }
        if connection is not None:
            self._values["connection"] = connection
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if for_each is not None:
            self._values["for_each"] = for_each
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider
        if provisioners is not None:
            self._values["provisioners"] = provisioners
        if app_status_poll_seconds is not None:
            self._values["app_status_poll_seconds"] = app_status_poll_seconds
        if git_auth_basic is not None:
            self._values["git_auth_basic"] = git_auth_basic
        if git_auth_ssh is not None:
            self._values["git_auth_ssh"] = git_auth_ssh
        if project_variables is not None:
            self._values["project_variables"] = project_variables
        if remote_runners_enabled is not None:
            self._values["remote_runners_enabled"] = remote_runners_enabled

    @builtins.property
    def connection(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, _cdktf_9a9027ec.WinrmProvisionerConnection]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("connection")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, _cdktf_9a9027ec.WinrmProvisionerConnection]], result)

    @builtins.property
    def count(
        self,
    ) -> typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("count")
        return typing.cast(typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]], result)

    @builtins.property
    def depends_on(
        self,
    ) -> typing.Optional[typing.List[_cdktf_9a9027ec.ITerraformDependable]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("depends_on")
        return typing.cast(typing.Optional[typing.List[_cdktf_9a9027ec.ITerraformDependable]], result)

    @builtins.property
    def for_each(self) -> typing.Optional[_cdktf_9a9027ec.ITerraformIterator]:
        '''
        :stability: experimental
        '''
        result = self._values.get("for_each")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.ITerraformIterator], result)

    @builtins.property
    def lifecycle(self) -> typing.Optional[_cdktf_9a9027ec.TerraformResourceLifecycle]:
        '''
        :stability: experimental
        '''
        result = self._values.get("lifecycle")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.TerraformResourceLifecycle], result)

    @builtins.property
    def provider(self) -> typing.Optional[_cdktf_9a9027ec.TerraformProvider]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provider")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.TerraformProvider], result)

    @builtins.property
    def provisioners(
        self,
    ) -> typing.Optional[typing.List[typing.Union[_cdktf_9a9027ec.FileProvisioner, _cdktf_9a9027ec.LocalExecProvisioner, _cdktf_9a9027ec.RemoteExecProvisioner]]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provisioners")
        return typing.cast(typing.Optional[typing.List[typing.Union[_cdktf_9a9027ec.FileProvisioner, _cdktf_9a9027ec.LocalExecProvisioner, _cdktf_9a9027ec.RemoteExecProvisioner]]], result)

    @builtins.property
    def data_source_git(self) -> "ProjectDataSourceGit":
        '''Configuration of Git repository where waypoint.hcl file is stored.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/waypoint/0.1.0/docs/resources/project#data_source_git Project#data_source_git}
        '''
        result = self._values.get("data_source_git")
        assert result is not None, "Required property 'data_source_git' is missing"
        return typing.cast("ProjectDataSourceGit", result)

    @builtins.property
    def project_name(self) -> builtins.str:
        '''The name of the Waypoint project.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/waypoint/0.1.0/docs/resources/project#project_name Project#project_name}
        '''
        result = self._values.get("project_name")
        assert result is not None, "Required property 'project_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def app_status_poll_seconds(self) -> typing.Optional[jsii.Number]:
        '''Application status poll interval in seconds.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/waypoint/0.1.0/docs/resources/project#app_status_poll_seconds Project#app_status_poll_seconds}
        '''
        result = self._values.get("app_status_poll_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def git_auth_basic(self) -> typing.Optional["ProjectGitAuthBasic"]:
        '''Basic authentication details for Git consisting of ``username`` and ``password``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/waypoint/0.1.0/docs/resources/project#git_auth_basic Project#git_auth_basic}
        '''
        result = self._values.get("git_auth_basic")
        return typing.cast(typing.Optional["ProjectGitAuthBasic"], result)

    @builtins.property
    def git_auth_ssh(self) -> typing.Optional["ProjectGitAuthSsh"]:
        '''SSH authentication details for Git.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/waypoint/0.1.0/docs/resources/project#git_auth_ssh Project#git_auth_ssh}
        '''
        result = self._values.get("git_auth_ssh")
        return typing.cast(typing.Optional["ProjectGitAuthSsh"], result)

    @builtins.property
    def project_variables(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ProjectProjectVariables"]]]:
        '''List of variables in Key/value pairs associated with the Waypoint Project.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/waypoint/0.1.0/docs/resources/project#project_variables Project#project_variables}
        '''
        result = self._values.get("project_variables")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ProjectProjectVariables"]]], result)

    @builtins.property
    def remote_runners_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enable remote runners for project.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/waypoint/0.1.0/docs/resources/project#remote_runners_enabled Project#remote_runners_enabled}
        '''
        result = self._values.get("remote_runners_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ProjectConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-waypoint.project.ProjectDataSourceGit",
    jsii_struct_bases=[],
    name_mapping={
        "file_change_signal": "fileChangeSignal",
        "git_path": "gitPath",
        "git_poll_interval_seconds": "gitPollIntervalSeconds",
        "git_ref": "gitRef",
        "git_url": "gitUrl",
        "ignore_changes_outside_path": "ignoreChangesOutsidePath",
    },
)
class ProjectDataSourceGit:
    def __init__(
        self,
        *,
        file_change_signal: typing.Optional[builtins.str] = None,
        git_path: typing.Optional[builtins.str] = None,
        git_poll_interval_seconds: typing.Optional[jsii.Number] = None,
        git_ref: typing.Optional[builtins.str] = None,
        git_url: typing.Optional[builtins.str] = None,
        ignore_changes_outside_path: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param file_change_signal: Indicates signal to be sent to any applications when their config files change. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/waypoint/0.1.0/docs/resources/project#file_change_signal Project#file_change_signal}
        :param git_path: Path in git repository when waypoint.hcl file is stored in a sub-directory. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/waypoint/0.1.0/docs/resources/project#git_path Project#git_path}
        :param git_poll_interval_seconds: Interval at which Waypoint should poll git repository for changes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/waypoint/0.1.0/docs/resources/project#git_poll_interval_seconds Project#git_poll_interval_seconds}
        :param git_ref: Git repository ref containing waypoint.hcl file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/waypoint/0.1.0/docs/resources/project#git_ref Project#git_ref}
        :param git_url: Url of git repository storing the waypoint.hcl file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/waypoint/0.1.0/docs/resources/project#git_url Project#git_url}
        :param ignore_changes_outside_path: Whether Waypoint ignores changes outside path storing waypoint.hcl file. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/waypoint/0.1.0/docs/resources/project#ignore_changes_outside_path Project#ignore_changes_outside_path}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1a5b2e3586a76243cfae086d3498df3363418fcfb6176eeea9b64e7d6ed0a2d)
            check_type(argname="argument file_change_signal", value=file_change_signal, expected_type=type_hints["file_change_signal"])
            check_type(argname="argument git_path", value=git_path, expected_type=type_hints["git_path"])
            check_type(argname="argument git_poll_interval_seconds", value=git_poll_interval_seconds, expected_type=type_hints["git_poll_interval_seconds"])
            check_type(argname="argument git_ref", value=git_ref, expected_type=type_hints["git_ref"])
            check_type(argname="argument git_url", value=git_url, expected_type=type_hints["git_url"])
            check_type(argname="argument ignore_changes_outside_path", value=ignore_changes_outside_path, expected_type=type_hints["ignore_changes_outside_path"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if file_change_signal is not None:
            self._values["file_change_signal"] = file_change_signal
        if git_path is not None:
            self._values["git_path"] = git_path
        if git_poll_interval_seconds is not None:
            self._values["git_poll_interval_seconds"] = git_poll_interval_seconds
        if git_ref is not None:
            self._values["git_ref"] = git_ref
        if git_url is not None:
            self._values["git_url"] = git_url
        if ignore_changes_outside_path is not None:
            self._values["ignore_changes_outside_path"] = ignore_changes_outside_path

    @builtins.property
    def file_change_signal(self) -> typing.Optional[builtins.str]:
        '''Indicates signal to be sent to any applications when their config files change.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/waypoint/0.1.0/docs/resources/project#file_change_signal Project#file_change_signal}
        '''
        result = self._values.get("file_change_signal")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def git_path(self) -> typing.Optional[builtins.str]:
        '''Path in git repository when waypoint.hcl file is stored in a sub-directory.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/waypoint/0.1.0/docs/resources/project#git_path Project#git_path}
        '''
        result = self._values.get("git_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def git_poll_interval_seconds(self) -> typing.Optional[jsii.Number]:
        '''Interval at which Waypoint should poll git repository for changes.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/waypoint/0.1.0/docs/resources/project#git_poll_interval_seconds Project#git_poll_interval_seconds}
        '''
        result = self._values.get("git_poll_interval_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def git_ref(self) -> typing.Optional[builtins.str]:
        '''Git repository ref containing waypoint.hcl file.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/waypoint/0.1.0/docs/resources/project#git_ref Project#git_ref}
        '''
        result = self._values.get("git_ref")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def git_url(self) -> typing.Optional[builtins.str]:
        '''Url of git repository storing the waypoint.hcl file.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/waypoint/0.1.0/docs/resources/project#git_url Project#git_url}
        '''
        result = self._values.get("git_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ignore_changes_outside_path(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether Waypoint ignores changes outside path storing waypoint.hcl file.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/waypoint/0.1.0/docs/resources/project#ignore_changes_outside_path Project#ignore_changes_outside_path}
        '''
        result = self._values.get("ignore_changes_outside_path")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ProjectDataSourceGit(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ProjectDataSourceGitOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-waypoint.project.ProjectDataSourceGitOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a05d7641f93055f04f631626a12c133155a754257848bb6a6d90c00c9d37ef66)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetFileChangeSignal")
    def reset_file_change_signal(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFileChangeSignal", []))

    @jsii.member(jsii_name="resetGitPath")
    def reset_git_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGitPath", []))

    @jsii.member(jsii_name="resetGitPollIntervalSeconds")
    def reset_git_poll_interval_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGitPollIntervalSeconds", []))

    @jsii.member(jsii_name="resetGitRef")
    def reset_git_ref(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGitRef", []))

    @jsii.member(jsii_name="resetGitUrl")
    def reset_git_url(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGitUrl", []))

    @jsii.member(jsii_name="resetIgnoreChangesOutsidePath")
    def reset_ignore_changes_outside_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIgnoreChangesOutsidePath", []))

    @builtins.property
    @jsii.member(jsii_name="fileChangeSignalInput")
    def file_change_signal_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fileChangeSignalInput"))

    @builtins.property
    @jsii.member(jsii_name="gitPathInput")
    def git_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "gitPathInput"))

    @builtins.property
    @jsii.member(jsii_name="gitPollIntervalSecondsInput")
    def git_poll_interval_seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "gitPollIntervalSecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="gitRefInput")
    def git_ref_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "gitRefInput"))

    @builtins.property
    @jsii.member(jsii_name="gitUrlInput")
    def git_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "gitUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="ignoreChangesOutsidePathInput")
    def ignore_changes_outside_path_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "ignoreChangesOutsidePathInput"))

    @builtins.property
    @jsii.member(jsii_name="fileChangeSignal")
    def file_change_signal(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fileChangeSignal"))

    @file_change_signal.setter
    def file_change_signal(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ee729dedd11882931b1dd73f6cfc69200c5e7fe6f3d6368a097b0e4156dc5af)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fileChangeSignal", value)

    @builtins.property
    @jsii.member(jsii_name="gitPath")
    def git_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "gitPath"))

    @git_path.setter
    def git_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d716e2e216f2aab26c66250b90655ab376db1f3a68fb9e962930739372dc798)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "gitPath", value)

    @builtins.property
    @jsii.member(jsii_name="gitPollIntervalSeconds")
    def git_poll_interval_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "gitPollIntervalSeconds"))

    @git_poll_interval_seconds.setter
    def git_poll_interval_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d28b86d4748c1be5c4855dd58a89d689f90190f1fdfb793463a894a05965b4d4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "gitPollIntervalSeconds", value)

    @builtins.property
    @jsii.member(jsii_name="gitRef")
    def git_ref(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "gitRef"))

    @git_ref.setter
    def git_ref(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0578224be585d255e16176e1781a1f0c23a4cb2e886eb0187dcaa993655db09)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "gitRef", value)

    @builtins.property
    @jsii.member(jsii_name="gitUrl")
    def git_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "gitUrl"))

    @git_url.setter
    def git_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a79f0f36771811991f8e437741391b6bea746c7c8dfce411ba0dea83a12740a1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "gitUrl", value)

    @builtins.property
    @jsii.member(jsii_name="ignoreChangesOutsidePath")
    def ignore_changes_outside_path(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "ignoreChangesOutsidePath"))

    @ignore_changes_outside_path.setter
    def ignore_changes_outside_path(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18017749101889f5dd05490d4e370b545e444d929415e0800b64f399c0f6c183)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ignoreChangesOutsidePath", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[ProjectDataSourceGit, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[ProjectDataSourceGit, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[ProjectDataSourceGit, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__55a6753df4b31619638b978e41d6fc693c77b71daa19bd22f9aec504c36c74c5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-waypoint.project.ProjectGitAuthBasic",
    jsii_struct_bases=[],
    name_mapping={"password": "password", "username": "username"},
)
class ProjectGitAuthBasic:
    def __init__(self, *, password: builtins.str, username: builtins.str) -> None:
        '''
        :param password: Git password. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/waypoint/0.1.0/docs/resources/project#password Project#password}
        :param username: Git username. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/waypoint/0.1.0/docs/resources/project#username Project#username}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7047220a8f7db363e8e9fca31ec8aa11763bb194a15c766e5d38cd80d7fcb567)
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
            check_type(argname="argument username", value=username, expected_type=type_hints["username"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "password": password,
            "username": username,
        }

    @builtins.property
    def password(self) -> builtins.str:
        '''Git password.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/waypoint/0.1.0/docs/resources/project#password Project#password}
        '''
        result = self._values.get("password")
        assert result is not None, "Required property 'password' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def username(self) -> builtins.str:
        '''Git username.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/waypoint/0.1.0/docs/resources/project#username Project#username}
        '''
        result = self._values.get("username")
        assert result is not None, "Required property 'username' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ProjectGitAuthBasic(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ProjectGitAuthBasicOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-waypoint.project.ProjectGitAuthBasicOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c89004c33b9deaba110c689ba6f49a5153589013ab8fc817bca7953ab643f43c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="passwordInput")
    def password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "passwordInput"))

    @builtins.property
    @jsii.member(jsii_name="usernameInput")
    def username_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "usernameInput"))

    @builtins.property
    @jsii.member(jsii_name="password")
    def password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "password"))

    @password.setter
    def password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ffadf108abd91a479449994886765a0284e2a2ddb3a90bcc90d52ad56e7ae9ba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "password", value)

    @builtins.property
    @jsii.member(jsii_name="username")
    def username(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "username"))

    @username.setter
    def username(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8699b1a9cc0b610a757c6b00a428ec61645e2e63aee1856350cfa0a68841cd7d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "username", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[ProjectGitAuthBasic, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[ProjectGitAuthBasic, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[ProjectGitAuthBasic, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6292fae11b1ba6ff60b1d476796e38e51b93d98196cf741d516e16b3d58baaed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-waypoint.project.ProjectGitAuthSsh",
    jsii_struct_bases=[],
    name_mapping={
        "ssh_private_key": "sshPrivateKey",
        "git_user": "gitUser",
        "passphrase": "passphrase",
    },
)
class ProjectGitAuthSsh:
    def __init__(
        self,
        *,
        ssh_private_key: builtins.str,
        git_user: typing.Optional[builtins.str] = None,
        passphrase: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param ssh_private_key: Private key to authenticate to Git. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/waypoint/0.1.0/docs/resources/project#ssh_private_key Project#ssh_private_key}
        :param git_user: Git user associated with private key. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/waypoint/0.1.0/docs/resources/project#git_user Project#git_user}
        :param passphrase: Passphrase to use with private key. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/waypoint/0.1.0/docs/resources/project#passphrase Project#passphrase}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c1ad87f1f2dca0d65d7f3d16792f2d968a60402b31339080906d5b86d694e90)
            check_type(argname="argument ssh_private_key", value=ssh_private_key, expected_type=type_hints["ssh_private_key"])
            check_type(argname="argument git_user", value=git_user, expected_type=type_hints["git_user"])
            check_type(argname="argument passphrase", value=passphrase, expected_type=type_hints["passphrase"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "ssh_private_key": ssh_private_key,
        }
        if git_user is not None:
            self._values["git_user"] = git_user
        if passphrase is not None:
            self._values["passphrase"] = passphrase

    @builtins.property
    def ssh_private_key(self) -> builtins.str:
        '''Private key to authenticate to Git.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/waypoint/0.1.0/docs/resources/project#ssh_private_key Project#ssh_private_key}
        '''
        result = self._values.get("ssh_private_key")
        assert result is not None, "Required property 'ssh_private_key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def git_user(self) -> typing.Optional[builtins.str]:
        '''Git user associated with private key.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/waypoint/0.1.0/docs/resources/project#git_user Project#git_user}
        '''
        result = self._values.get("git_user")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def passphrase(self) -> typing.Optional[builtins.str]:
        '''Passphrase to use with private key.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/waypoint/0.1.0/docs/resources/project#passphrase Project#passphrase}
        '''
        result = self._values.get("passphrase")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ProjectGitAuthSsh(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ProjectGitAuthSshOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-waypoint.project.ProjectGitAuthSshOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7c0b6e9d4d4b13acdb87d890537935add9acd3a15003fb8d087da5cfa43cb7f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetGitUser")
    def reset_git_user(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGitUser", []))

    @jsii.member(jsii_name="resetPassphrase")
    def reset_passphrase(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPassphrase", []))

    @builtins.property
    @jsii.member(jsii_name="gitUserInput")
    def git_user_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "gitUserInput"))

    @builtins.property
    @jsii.member(jsii_name="passphraseInput")
    def passphrase_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "passphraseInput"))

    @builtins.property
    @jsii.member(jsii_name="sshPrivateKeyInput")
    def ssh_private_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sshPrivateKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="gitUser")
    def git_user(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "gitUser"))

    @git_user.setter
    def git_user(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0785eda122cb787894e3beba2b1dc1964907cdb8cede2e6ac00762fefe08b156)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "gitUser", value)

    @builtins.property
    @jsii.member(jsii_name="passphrase")
    def passphrase(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "passphrase"))

    @passphrase.setter
    def passphrase(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b6a1bdacc10dcf112029d2981b61991bf12e7629c96a8907ffd4e489b840da3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "passphrase", value)

    @builtins.property
    @jsii.member(jsii_name="sshPrivateKey")
    def ssh_private_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sshPrivateKey"))

    @ssh_private_key.setter
    def ssh_private_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e5753a309769dfa418bf89d6cdacb22fd4893ef243bbcc538381722d5206219a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sshPrivateKey", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[ProjectGitAuthSsh, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[ProjectGitAuthSsh, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[ProjectGitAuthSsh, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6be3fab714a531c1ed0c41f5ff3d35036f229f31b48a0809a2bd899cd116eb5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-waypoint.project.ProjectProjectVariables",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "value": "value", "sensitive": "sensitive"},
)
class ProjectProjectVariables:
    def __init__(
        self,
        *,
        name: builtins.str,
        value: builtins.str,
        sensitive: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/waypoint/0.1.0/docs/resources/project#name Project#name}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/waypoint/0.1.0/docs/resources/project#value Project#value}.
        :param sensitive: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/waypoint/0.1.0/docs/resources/project#sensitive Project#sensitive}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6129604cf1b0a9c6bce00db10163600976a4bb82ecec1acd825ecfb82403bc98)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            check_type(argname="argument sensitive", value=sensitive, expected_type=type_hints["sensitive"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "value": value,
        }
        if sensitive is not None:
            self._values["sensitive"] = sensitive

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/waypoint/0.1.0/docs/resources/project#name Project#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/waypoint/0.1.0/docs/resources/project#value Project#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def sensitive(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/waypoint/0.1.0/docs/resources/project#sensitive Project#sensitive}.'''
        result = self._values.get("sensitive")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ProjectProjectVariables(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ProjectProjectVariablesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-waypoint.project.ProjectProjectVariablesList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e25aece0723ae922c00b6926ec78d0d4320253db313a50e5d456edd30bb07386)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "ProjectProjectVariablesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ac345c15cf549a90f11434661471493924683432fd1778a79410f9a7ce37bb6)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ProjectProjectVariablesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00ead5daef719238a99fcd63a31e835d0b3a27cafbd16cc1322d1ec7461ae69a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value)

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac051e9d9422be1519ad0393c590052509bf69f3f1f10de9456fc171b3ea3d2d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value)

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__abe3a7ffcfc7760cf58218020882d4a2e34025e35e8243345d0d6647feb28932)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ProjectProjectVariables]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ProjectProjectVariables]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ProjectProjectVariables]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59f29e3da65efd4b97921c2cec4a15d72c7b562bed11c99c2abd93ca948f8a77)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class ProjectProjectVariablesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-waypoint.project.ProjectProjectVariablesOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c714d096064d7c77d8b39c1152cf0c63d41819dcb77ce4f16b527902dfaa5b7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetSensitive")
    def reset_sensitive(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSensitive", []))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="sensitiveInput")
    def sensitive_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "sensitiveInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3bd97f9a9683a548e56e98ed4527004dafefb794c2a76d963e5162bd1a8fda83)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="sensitive")
    def sensitive(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "sensitive"))

    @sensitive.setter
    def sensitive(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d48552ada7382a91418d0880c4496d14a3cb05d1c25defcab9baaef3b83bb88d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sensitive", value)

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09988f936d7a1bab4c56294dce47635d64799f00ff6361aa5d2a13bbf0fa624a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[ProjectProjectVariables, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[ProjectProjectVariables, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[ProjectProjectVariables, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__080c9a30fc3b05708a0cc8458dc17fbb45137b8463550d34852d76f28766ef97)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "Project",
    "ProjectConfig",
    "ProjectDataSourceGit",
    "ProjectDataSourceGitOutputReference",
    "ProjectGitAuthBasic",
    "ProjectGitAuthBasicOutputReference",
    "ProjectGitAuthSsh",
    "ProjectGitAuthSshOutputReference",
    "ProjectProjectVariables",
    "ProjectProjectVariablesList",
    "ProjectProjectVariablesOutputReference",
]

publication.publish()

def _typecheckingstub__fb9746c0aa81d9d3480a2fa32af683247b737ead912768d1626c69fac220b8a7(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    data_source_git: typing.Union[ProjectDataSourceGit, typing.Dict[builtins.str, typing.Any]],
    project_name: builtins.str,
    app_status_poll_seconds: typing.Optional[jsii.Number] = None,
    git_auth_basic: typing.Optional[typing.Union[ProjectGitAuthBasic, typing.Dict[builtins.str, typing.Any]]] = None,
    git_auth_ssh: typing.Optional[typing.Union[ProjectGitAuthSsh, typing.Dict[builtins.str, typing.Any]]] = None,
    project_variables: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ProjectProjectVariables, typing.Dict[builtins.str, typing.Any]]]]] = None,
    remote_runners_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eac4a7f77e3f693bbe518a0736f5b7fe6127b8f3f5a9c4591e229b75ba49cdb8(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ProjectProjectVariables, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__125d3794b58343c1eae21755088dff39db9e7c5d667f4d91ef8be1433850b484(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14c5e0c5be3f3d8c70bcfc75df9cc09e59376281b18b0773815a6e23e775da1a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8a2c85809413f806769509b6ac4dbe415635431063b17849bf3877fa51ed3c0(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3fb662a4b6582b2cd24299d38f0e68455d5bd6fbea6b15350775e5fcf482b60b(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    data_source_git: typing.Union[ProjectDataSourceGit, typing.Dict[builtins.str, typing.Any]],
    project_name: builtins.str,
    app_status_poll_seconds: typing.Optional[jsii.Number] = None,
    git_auth_basic: typing.Optional[typing.Union[ProjectGitAuthBasic, typing.Dict[builtins.str, typing.Any]]] = None,
    git_auth_ssh: typing.Optional[typing.Union[ProjectGitAuthSsh, typing.Dict[builtins.str, typing.Any]]] = None,
    project_variables: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ProjectProjectVariables, typing.Dict[builtins.str, typing.Any]]]]] = None,
    remote_runners_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1a5b2e3586a76243cfae086d3498df3363418fcfb6176eeea9b64e7d6ed0a2d(
    *,
    file_change_signal: typing.Optional[builtins.str] = None,
    git_path: typing.Optional[builtins.str] = None,
    git_poll_interval_seconds: typing.Optional[jsii.Number] = None,
    git_ref: typing.Optional[builtins.str] = None,
    git_url: typing.Optional[builtins.str] = None,
    ignore_changes_outside_path: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a05d7641f93055f04f631626a12c133155a754257848bb6a6d90c00c9d37ef66(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ee729dedd11882931b1dd73f6cfc69200c5e7fe6f3d6368a097b0e4156dc5af(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d716e2e216f2aab26c66250b90655ab376db1f3a68fb9e962930739372dc798(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d28b86d4748c1be5c4855dd58a89d689f90190f1fdfb793463a894a05965b4d4(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0578224be585d255e16176e1781a1f0c23a4cb2e886eb0187dcaa993655db09(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a79f0f36771811991f8e437741391b6bea746c7c8dfce411ba0dea83a12740a1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18017749101889f5dd05490d4e370b545e444d929415e0800b64f399c0f6c183(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55a6753df4b31619638b978e41d6fc693c77b71daa19bd22f9aec504c36c74c5(
    value: typing.Optional[typing.Union[ProjectDataSourceGit, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7047220a8f7db363e8e9fca31ec8aa11763bb194a15c766e5d38cd80d7fcb567(
    *,
    password: builtins.str,
    username: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c89004c33b9deaba110c689ba6f49a5153589013ab8fc817bca7953ab643f43c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ffadf108abd91a479449994886765a0284e2a2ddb3a90bcc90d52ad56e7ae9ba(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8699b1a9cc0b610a757c6b00a428ec61645e2e63aee1856350cfa0a68841cd7d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6292fae11b1ba6ff60b1d476796e38e51b93d98196cf741d516e16b3d58baaed(
    value: typing.Optional[typing.Union[ProjectGitAuthBasic, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c1ad87f1f2dca0d65d7f3d16792f2d968a60402b31339080906d5b86d694e90(
    *,
    ssh_private_key: builtins.str,
    git_user: typing.Optional[builtins.str] = None,
    passphrase: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7c0b6e9d4d4b13acdb87d890537935add9acd3a15003fb8d087da5cfa43cb7f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0785eda122cb787894e3beba2b1dc1964907cdb8cede2e6ac00762fefe08b156(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b6a1bdacc10dcf112029d2981b61991bf12e7629c96a8907ffd4e489b840da3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5753a309769dfa418bf89d6cdacb22fd4893ef243bbcc538381722d5206219a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6be3fab714a531c1ed0c41f5ff3d35036f229f31b48a0809a2bd899cd116eb5(
    value: typing.Optional[typing.Union[ProjectGitAuthSsh, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6129604cf1b0a9c6bce00db10163600976a4bb82ecec1acd825ecfb82403bc98(
    *,
    name: builtins.str,
    value: builtins.str,
    sensitive: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e25aece0723ae922c00b6926ec78d0d4320253db313a50e5d456edd30bb07386(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ac345c15cf549a90f11434661471493924683432fd1778a79410f9a7ce37bb6(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00ead5daef719238a99fcd63a31e835d0b3a27cafbd16cc1322d1ec7461ae69a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac051e9d9422be1519ad0393c590052509bf69f3f1f10de9456fc171b3ea3d2d(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abe3a7ffcfc7760cf58218020882d4a2e34025e35e8243345d0d6647feb28932(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59f29e3da65efd4b97921c2cec4a15d72c7b562bed11c99c2abd93ca948f8a77(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ProjectProjectVariables]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c714d096064d7c77d8b39c1152cf0c63d41819dcb77ce4f16b527902dfaa5b7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3bd97f9a9683a548e56e98ed4527004dafefb794c2a76d963e5162bd1a8fda83(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d48552ada7382a91418d0880c4496d14a3cb05d1c25defcab9baaef3b83bb88d(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09988f936d7a1bab4c56294dce47635d64799f00ff6361aa5d2a13bbf0fa624a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__080c9a30fc3b05708a0cc8458dc17fbb45137b8463550d34852d76f28766ef97(
    value: typing.Optional[typing.Union[ProjectProjectVariables, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass
