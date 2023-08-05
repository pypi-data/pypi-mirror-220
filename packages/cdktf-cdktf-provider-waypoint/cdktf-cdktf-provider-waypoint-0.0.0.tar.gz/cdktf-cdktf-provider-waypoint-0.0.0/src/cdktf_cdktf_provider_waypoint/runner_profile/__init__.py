'''
# `waypoint_runner_profile`

Refer to the Terraform Registory for docs: [`waypoint_runner_profile`](https://registry.terraform.io/providers/hashicorp/waypoint/0.1.0/docs/resources/runner_profile).
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


class RunnerProfile(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-waypoint.runnerProfile.RunnerProfile",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/waypoint/0.1.0/docs/resources/runner_profile waypoint_runner_profile}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        name: builtins.str,
        plugin_type: builtins.str,
        default: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        environment_variables: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        oci_url: typing.Optional[builtins.str] = None,
        plugin_config: typing.Optional[builtins.str] = None,
        plugin_config_format: typing.Optional[builtins.str] = None,
        target_runner_id: typing.Optional[builtins.str] = None,
        target_runner_labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/waypoint/0.1.0/docs/resources/runner_profile waypoint_runner_profile} Resource.

        :param scope: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: The name of the runner profile. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/waypoint/0.1.0/docs/resources/runner_profile#name RunnerProfile#name}
        :param plugin_type: Plugin type for runner i.e docker / kubernetes / aws-ecs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/waypoint/0.1.0/docs/resources/runner_profile#plugin_type RunnerProfile#plugin_type}
        :param default: Indicates if this runner profile is the default for any new projects. The default is false. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/waypoint/0.1.0/docs/resources/runner_profile#default RunnerProfile#default}
        :param environment_variables: Any environment variables that should be exposed to the on demand runner. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/waypoint/0.1.0/docs/resources/runner_profile#environment_variables RunnerProfile#environment_variables}
        :param oci_url: oci_url is the OCI image that will be used to boot the on demand runner. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/waypoint/0.1.0/docs/resources/runner_profile#oci_url RunnerProfile#oci_url}
        :param plugin_config: Plugin config is the configuration for the plugin that is created. It is usually HCL and is decoded like the other plugins, and is plugin specific. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/waypoint/0.1.0/docs/resources/runner_profile#plugin_config RunnerProfile#plugin_config}
        :param plugin_config_format: Config format specifies the format of plugin_config. Valid values are HCL or JSON. The default is HCL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/waypoint/0.1.0/docs/resources/runner_profile#plugin_config_format RunnerProfile#plugin_config_format}
        :param target_runner_id: The ID of the target runner for this profile. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/waypoint/0.1.0/docs/resources/runner_profile#target_runner_id RunnerProfile#target_runner_id}
        :param target_runner_labels: A map of labels on target runners. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/waypoint/0.1.0/docs/resources/runner_profile#target_runner_labels RunnerProfile#target_runner_labels}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__355d3fdfcf75061abfdcae18400572543b3678e202b1146ae40a643e76cf357e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        config = RunnerProfileConfig(
            name=name,
            plugin_type=plugin_type,
            default=default,
            environment_variables=environment_variables,
            oci_url=oci_url,
            plugin_config=plugin_config,
            plugin_config_format=plugin_config_format,
            target_runner_id=target_runner_id,
            target_runner_labels=target_runner_labels,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id, config])

    @jsii.member(jsii_name="resetDefault")
    def reset_default(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefault", []))

    @jsii.member(jsii_name="resetEnvironmentVariables")
    def reset_environment_variables(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnvironmentVariables", []))

    @jsii.member(jsii_name="resetOciUrl")
    def reset_oci_url(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOciUrl", []))

    @jsii.member(jsii_name="resetPluginConfig")
    def reset_plugin_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPluginConfig", []))

    @jsii.member(jsii_name="resetPluginConfigFormat")
    def reset_plugin_config_format(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPluginConfigFormat", []))

    @jsii.member(jsii_name="resetTargetRunnerId")
    def reset_target_runner_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTargetRunnerId", []))

    @jsii.member(jsii_name="resetTargetRunnerLabels")
    def reset_target_runner_labels(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTargetRunnerLabels", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="defaultInput")
    def default_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "defaultInput"))

    @builtins.property
    @jsii.member(jsii_name="environmentVariablesInput")
    def environment_variables_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "environmentVariablesInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="ociUrlInput")
    def oci_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ociUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="pluginConfigFormatInput")
    def plugin_config_format_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pluginConfigFormatInput"))

    @builtins.property
    @jsii.member(jsii_name="pluginConfigInput")
    def plugin_config_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pluginConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="pluginTypeInput")
    def plugin_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pluginTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="targetRunnerIdInput")
    def target_runner_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "targetRunnerIdInput"))

    @builtins.property
    @jsii.member(jsii_name="targetRunnerLabelsInput")
    def target_runner_labels_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "targetRunnerLabelsInput"))

    @builtins.property
    @jsii.member(jsii_name="default")
    def default(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "default"))

    @default.setter
    def default(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__249c805acf16c5484af90ac3b8b04c7dd0ee5945b2ef2b99475a9da0c177db21)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "default", value)

    @builtins.property
    @jsii.member(jsii_name="environmentVariables")
    def environment_variables(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "environmentVariables"))

    @environment_variables.setter
    def environment_variables(
        self,
        value: typing.Mapping[builtins.str, builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf69d543bafd75582e5cc988c63dd747d52c69225b893daf0d1addff88d99154)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "environmentVariables", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25c21247c6924d28b6594796932dc983a264020ed7cf563b64b7cd52e9c3d7a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="ociUrl")
    def oci_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ociUrl"))

    @oci_url.setter
    def oci_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7bba6712ed2ad925af34352743f904921dd1329f6820233edaad569619c4ab9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ociUrl", value)

    @builtins.property
    @jsii.member(jsii_name="pluginConfig")
    def plugin_config(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pluginConfig"))

    @plugin_config.setter
    def plugin_config(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__264a1326dc06afbd795281c03879181b5d1db36d0773cb1bedbcb52be8822a48)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pluginConfig", value)

    @builtins.property
    @jsii.member(jsii_name="pluginConfigFormat")
    def plugin_config_format(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pluginConfigFormat"))

    @plugin_config_format.setter
    def plugin_config_format(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eae89aeb1ff155c84fdcacd7c5e42ba3f50baf76c47eb29b3f21c0858ce32f00)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pluginConfigFormat", value)

    @builtins.property
    @jsii.member(jsii_name="pluginType")
    def plugin_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pluginType"))

    @plugin_type.setter
    def plugin_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__439d9cc772dd79613c27cddb96af404a77b4ab5d79b1bf346223870495a86910)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pluginType", value)

    @builtins.property
    @jsii.member(jsii_name="targetRunnerId")
    def target_runner_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "targetRunnerId"))

    @target_runner_id.setter
    def target_runner_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79ccd8e320b82515906b465f9687a130bc89c466423bb8a41e13f2c8cb088cc9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetRunnerId", value)

    @builtins.property
    @jsii.member(jsii_name="targetRunnerLabels")
    def target_runner_labels(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "targetRunnerLabels"))

    @target_runner_labels.setter
    def target_runner_labels(
        self,
        value: typing.Mapping[builtins.str, builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c6b0aeac2be802ec9422a299b3ead101ed45371e900fa84f51b0dcf9616a902b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetRunnerLabels", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-waypoint.runnerProfile.RunnerProfileConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "name": "name",
        "plugin_type": "pluginType",
        "default": "default",
        "environment_variables": "environmentVariables",
        "oci_url": "ociUrl",
        "plugin_config": "pluginConfig",
        "plugin_config_format": "pluginConfigFormat",
        "target_runner_id": "targetRunnerId",
        "target_runner_labels": "targetRunnerLabels",
    },
)
class RunnerProfileConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        name: builtins.str,
        plugin_type: builtins.str,
        default: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        environment_variables: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        oci_url: typing.Optional[builtins.str] = None,
        plugin_config: typing.Optional[builtins.str] = None,
        plugin_config_format: typing.Optional[builtins.str] = None,
        target_runner_id: typing.Optional[builtins.str] = None,
        target_runner_labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: The name of the runner profile. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/waypoint/0.1.0/docs/resources/runner_profile#name RunnerProfile#name}
        :param plugin_type: Plugin type for runner i.e docker / kubernetes / aws-ecs. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/waypoint/0.1.0/docs/resources/runner_profile#plugin_type RunnerProfile#plugin_type}
        :param default: Indicates if this runner profile is the default for any new projects. The default is false. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/waypoint/0.1.0/docs/resources/runner_profile#default RunnerProfile#default}
        :param environment_variables: Any environment variables that should be exposed to the on demand runner. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/waypoint/0.1.0/docs/resources/runner_profile#environment_variables RunnerProfile#environment_variables}
        :param oci_url: oci_url is the OCI image that will be used to boot the on demand runner. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/waypoint/0.1.0/docs/resources/runner_profile#oci_url RunnerProfile#oci_url}
        :param plugin_config: Plugin config is the configuration for the plugin that is created. It is usually HCL and is decoded like the other plugins, and is plugin specific. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/waypoint/0.1.0/docs/resources/runner_profile#plugin_config RunnerProfile#plugin_config}
        :param plugin_config_format: Config format specifies the format of plugin_config. Valid values are HCL or JSON. The default is HCL. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/waypoint/0.1.0/docs/resources/runner_profile#plugin_config_format RunnerProfile#plugin_config_format}
        :param target_runner_id: The ID of the target runner for this profile. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/waypoint/0.1.0/docs/resources/runner_profile#target_runner_id RunnerProfile#target_runner_id}
        :param target_runner_labels: A map of labels on target runners. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/waypoint/0.1.0/docs/resources/runner_profile#target_runner_labels RunnerProfile#target_runner_labels}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2350f8e08487187cec54dae72d019ff77b946e8f7564a27a786e0e0332fefe0)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument plugin_type", value=plugin_type, expected_type=type_hints["plugin_type"])
            check_type(argname="argument default", value=default, expected_type=type_hints["default"])
            check_type(argname="argument environment_variables", value=environment_variables, expected_type=type_hints["environment_variables"])
            check_type(argname="argument oci_url", value=oci_url, expected_type=type_hints["oci_url"])
            check_type(argname="argument plugin_config", value=plugin_config, expected_type=type_hints["plugin_config"])
            check_type(argname="argument plugin_config_format", value=plugin_config_format, expected_type=type_hints["plugin_config_format"])
            check_type(argname="argument target_runner_id", value=target_runner_id, expected_type=type_hints["target_runner_id"])
            check_type(argname="argument target_runner_labels", value=target_runner_labels, expected_type=type_hints["target_runner_labels"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "plugin_type": plugin_type,
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
        if default is not None:
            self._values["default"] = default
        if environment_variables is not None:
            self._values["environment_variables"] = environment_variables
        if oci_url is not None:
            self._values["oci_url"] = oci_url
        if plugin_config is not None:
            self._values["plugin_config"] = plugin_config
        if plugin_config_format is not None:
            self._values["plugin_config_format"] = plugin_config_format
        if target_runner_id is not None:
            self._values["target_runner_id"] = target_runner_id
        if target_runner_labels is not None:
            self._values["target_runner_labels"] = target_runner_labels

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
    def name(self) -> builtins.str:
        '''The name of the runner profile.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/waypoint/0.1.0/docs/resources/runner_profile#name RunnerProfile#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def plugin_type(self) -> builtins.str:
        '''Plugin type for runner i.e docker / kubernetes / aws-ecs.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/waypoint/0.1.0/docs/resources/runner_profile#plugin_type RunnerProfile#plugin_type}
        '''
        result = self._values.get("plugin_type")
        assert result is not None, "Required property 'plugin_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def default(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Indicates if this runner profile is the default for any new projects. The default is false.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/waypoint/0.1.0/docs/resources/runner_profile#default RunnerProfile#default}
        '''
        result = self._values.get("default")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def environment_variables(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Any environment variables that should be exposed to the on demand runner.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/waypoint/0.1.0/docs/resources/runner_profile#environment_variables RunnerProfile#environment_variables}
        '''
        result = self._values.get("environment_variables")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def oci_url(self) -> typing.Optional[builtins.str]:
        '''oci_url is the OCI image that will be used to boot the on demand runner.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/waypoint/0.1.0/docs/resources/runner_profile#oci_url RunnerProfile#oci_url}
        '''
        result = self._values.get("oci_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def plugin_config(self) -> typing.Optional[builtins.str]:
        '''Plugin config is the configuration for the plugin that is created.

        It is usually HCL and is decoded like the other plugins, and is plugin specific.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/waypoint/0.1.0/docs/resources/runner_profile#plugin_config RunnerProfile#plugin_config}
        '''
        result = self._values.get("plugin_config")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def plugin_config_format(self) -> typing.Optional[builtins.str]:
        '''Config format specifies the format of plugin_config. Valid values are HCL or JSON. The default is HCL.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/waypoint/0.1.0/docs/resources/runner_profile#plugin_config_format RunnerProfile#plugin_config_format}
        '''
        result = self._values.get("plugin_config_format")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def target_runner_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the target runner for this profile.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/waypoint/0.1.0/docs/resources/runner_profile#target_runner_id RunnerProfile#target_runner_id}
        '''
        result = self._values.get("target_runner_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def target_runner_labels(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''A map of labels on target runners.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/waypoint/0.1.0/docs/resources/runner_profile#target_runner_labels RunnerProfile#target_runner_labels}
        '''
        result = self._values.get("target_runner_labels")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RunnerProfileConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "RunnerProfile",
    "RunnerProfileConfig",
]

publication.publish()

def _typecheckingstub__355d3fdfcf75061abfdcae18400572543b3678e202b1146ae40a643e76cf357e(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    name: builtins.str,
    plugin_type: builtins.str,
    default: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    environment_variables: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    oci_url: typing.Optional[builtins.str] = None,
    plugin_config: typing.Optional[builtins.str] = None,
    plugin_config_format: typing.Optional[builtins.str] = None,
    target_runner_id: typing.Optional[builtins.str] = None,
    target_runner_labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
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

def _typecheckingstub__249c805acf16c5484af90ac3b8b04c7dd0ee5945b2ef2b99475a9da0c177db21(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf69d543bafd75582e5cc988c63dd747d52c69225b893daf0d1addff88d99154(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25c21247c6924d28b6594796932dc983a264020ed7cf563b64b7cd52e9c3d7a8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7bba6712ed2ad925af34352743f904921dd1329f6820233edaad569619c4ab9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__264a1326dc06afbd795281c03879181b5d1db36d0773cb1bedbcb52be8822a48(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eae89aeb1ff155c84fdcacd7c5e42ba3f50baf76c47eb29b3f21c0858ce32f00(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__439d9cc772dd79613c27cddb96af404a77b4ab5d79b1bf346223870495a86910(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79ccd8e320b82515906b465f9687a130bc89c466423bb8a41e13f2c8cb088cc9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6b0aeac2be802ec9422a299b3ead101ed45371e900fa84f51b0dcf9616a902b(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2350f8e08487187cec54dae72d019ff77b946e8f7564a27a786e0e0332fefe0(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    plugin_type: builtins.str,
    default: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    environment_variables: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    oci_url: typing.Optional[builtins.str] = None,
    plugin_config: typing.Optional[builtins.str] = None,
    plugin_config_format: typing.Optional[builtins.str] = None,
    target_runner_id: typing.Optional[builtins.str] = None,
    target_runner_labels: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass
