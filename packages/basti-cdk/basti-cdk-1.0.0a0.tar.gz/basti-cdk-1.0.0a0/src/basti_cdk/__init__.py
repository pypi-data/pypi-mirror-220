'''
# Basti CDK

Basti CDK is a library that provides constructs for AWS CDK that allow you to easily create a Basti instance within your existing infrastructure.

## The purpose of this construct

The purpose of this construct is to allow you to easily create a Basti instance within your existing infrastructure.
It provides all the benefits of using the Basti CLI while still having the ability to manage your infrastructure as you would any other infrastucture.
Integrating basti in IaC adds transparently to your application giving you and your team a better overview.

## Installation

The Construct is available in both TypeScript and Python, through the use of [jsii](https://github.com/aws/jsii).

npm:

```bash
npm install basti-cdk
```

python:

```bash
pip install basti-cdk
```

### Example

The example below is a simple setup of a basti instance and an RDS instance.
The construct can be modified but this is the simplest way to get started.

```python
const app = new cdk.App();
const bastiStack = new cdk.Stack(app, 'bastiStack');

// VPC to deploy basti into
const bastiVpc = new aws_ec2.Vpc(bastiStack, 'bastiVpc', {});

// Special basti security group
const bastiAccessSecurityGroup = new BastiAccessSecurityGroup(
  bastiStack,
  'bastiAccessSecurityGroup',
  {
    vpc: bastiVpc,
  }
);

// The basti instance itself
const bastiInstance = new BastiInstance(bastiStack, 'basti', {
  vpc: bastiVpc,
});

// An RDS instance to test basti with
const rdsInstance = new aws_rds.DatabaseInstance(
  bastiStack,
  'rdsInstance',
  {
    vpc: bastiVpc,
    engine: aws_rds.DatabaseInstanceEngine.POSTGRES,
    instanceType: aws_ec2.InstanceType.of(
      aws_ec2.InstanceClass.BURSTABLE2,
      aws_ec2.InstanceSize.MICRO
    ),
    // Here basti takes the security group we created earlier
    securityGroups: [bastiAccessSecurityGroup],
    port: 5432,
  }
);

// We then allow the basti instance access to the port of the RDS instance
bastiAccessSecurityGroup.addBastiInstance(
  // basti instance we created earlier
  bastiInstance,
  // Port can also be defined manually if needed
  aws_ec2.Port.tcp(rdsInstance.instanceEndpoint.port)
);
```

The basti instance can also allow roles to connect to it with the `grantBastiCliConnect` method.
You can also use this method to give groups/users permissions to connect to basti.

```python
// The basti instance itself
import {BastiInstance} from "basti-cdk";

const bastiInstance = new BastiInstance(...);
const role = new aws_iam.Role(...);

// Gives all the requires permissions to connect to the basti instance. With the direct conection option.
bastiInstance.grantBastiCliConnect(role);
```

An interface version of basti can also be created using `BastiInstance.fromBastiId(...)`. This method can be used
if your application is spread out over multiple projects.

```python
const app = new cdk.App();

const bastiStack = new cdk.Stack(app, 'bastiStack', {
    env: {
        account: '123456789012',
        region: 'us-east-1',
    },
});

// Ok so importing a security group (which is done when calling .fromBastiId)
// requires a vpc to be passed in without tokens.
// There is no way around this. So we "import" the vpc again. Again without tokens.
// it must have a fixed name.
const importedVpc = aws_ec2.Vpc.fromLookup(bastiStack, 'importedVpc', {
    vpcName: 'importedVpc',
});

const importedBastiInstance = BastiInstance.fromBastiId(
    bastiStack,
    'importedBastiInstance',
    'TEST_ID',
    importedVpc
);
```

## License

Usage is provided under the MIT License. See [LICENSE](https://github.com/BohdanPetryshyn/basti/blob/main/LICENSE) for the full details.
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

from ._jsii import *

import aws_cdk.aws_ec2 as _aws_cdk_aws_ec2_ceddda9d
import aws_cdk.aws_iam as _aws_cdk_aws_iam_ceddda9d
import constructs as _constructs_77d1e7e8


class BastiAccessSecurityGroup(
    _aws_cdk_aws_ec2_ceddda9d.SecurityGroup,
    metaclass=jsii.JSIIMeta,
    jsii_type="basti-cdk.BastiAccessSecurityGroup",
):
    '''The security group for the bastion instance.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        basti_id: typing.Optional[builtins.str] = None,
        vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
        allow_all_ipv6_outbound: typing.Optional[builtins.bool] = None,
        allow_all_outbound: typing.Optional[builtins.bool] = None,
        description: typing.Optional[builtins.str] = None,
        disable_inline_rules: typing.Optional[builtins.bool] = None,
        security_group_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Constructs a new instance of the BastiAccessSecurityGroup class.

        :param scope: The scope of the construct.
        :param id: The ID of the construct.
        :param basti_id: Basti ID. This ID is used as a suffix for the name, it is not the ID of the basti instance. Default: - A 8-character pseudo-random string
        :param vpc: The VPC in which to create the security group.
        :param allow_all_ipv6_outbound: Whether to allow all outbound ipv6 traffic by default. If this is set to true, there will only be a single egress rule which allows all outbound ipv6 traffic. If this is set to false, no outbound traffic will be allowed by default and all egress ipv6 traffic must be explicitly authorized. To allow all ipv4 traffic use allowAllOutbound Default: false
        :param allow_all_outbound: Whether to allow all outbound traffic by default. If this is set to true, there will only be a single egress rule which allows all outbound traffic. If this is set to false, no outbound traffic will be allowed by default and all egress traffic must be explicitly authorized. To allow all ipv6 traffic use allowAllIpv6Outbound Default: true
        :param description: A description of the security group. Default: The default name will be the construct's CDK path.
        :param disable_inline_rules: Whether to disable inline ingress and egress rule optimization. If this is set to true, ingress and egress rules will not be declared under the SecurityGroup in cloudformation, but will be separate elements. Inlining rules is an optimization for producing smaller stack templates. Sometimes this is not desirable, for example when security group access is managed via tags. The default value can be overriden globally by setting the context variable '@aws-cdk/aws-ec2.securityGroupDisableInlineRules'. Default: false
        :param security_group_name: The name of the security group. For valid values, see the GroupName parameter of the CreateSecurityGroup action in the Amazon EC2 API Reference. It is not recommended to use an explicit group name. Default: If you don't specify a GroupName, AWS CloudFormation generates a unique physical ID and uses that ID for the group name.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01948589ed1a60919700df630bf7069a9d8c730904dc0053525f1ca445fc0678)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = BastiAccessSecurityGroupProps(
            basti_id=basti_id,
            vpc=vpc,
            allow_all_ipv6_outbound=allow_all_ipv6_outbound,
            allow_all_outbound=allow_all_outbound,
            description=description,
            disable_inline_rules=disable_inline_rules,
            security_group_name=security_group_name,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="allowBastiInstanceConnection")
    def allow_basti_instance_connection(
        self,
        basti_instance: "IBastiInstance",
        port: _aws_cdk_aws_ec2_ceddda9d.Port,
    ) -> None:
        '''Adds an ingress rule to the security group.

        That allows the
        bastion instance to access the target instance.

        :param basti_instance: The Basti instance.
        :param port: The port to allow access to.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d033d471ed35bb19d7d2268c0a4a86abc74b88e32fdb3c7330adb7ad118b4dd)
            check_type(argname="argument basti_instance", value=basti_instance, expected_type=type_hints["basti_instance"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
        return typing.cast(None, jsii.invoke(self, "allowBastiInstanceConnection", [basti_instance, port]))

    @builtins.property
    @jsii.member(jsii_name="bastiId")
    def basti_id(self) -> builtins.str:
        '''The basti custom ID for the security group.'''
        return typing.cast(builtins.str, jsii.get(self, "bastiId"))


@jsii.data_type(
    jsii_type="basti-cdk.BastiAccessSecurityGroupProps",
    jsii_struct_bases=[_aws_cdk_aws_ec2_ceddda9d.SecurityGroupProps],
    name_mapping={
        "vpc": "vpc",
        "allow_all_ipv6_outbound": "allowAllIpv6Outbound",
        "allow_all_outbound": "allowAllOutbound",
        "description": "description",
        "disable_inline_rules": "disableInlineRules",
        "security_group_name": "securityGroupName",
        "basti_id": "bastiId",
    },
)
class BastiAccessSecurityGroupProps(_aws_cdk_aws_ec2_ceddda9d.SecurityGroupProps):
    def __init__(
        self,
        *,
        vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
        allow_all_ipv6_outbound: typing.Optional[builtins.bool] = None,
        allow_all_outbound: typing.Optional[builtins.bool] = None,
        description: typing.Optional[builtins.str] = None,
        disable_inline_rules: typing.Optional[builtins.bool] = None,
        security_group_name: typing.Optional[builtins.str] = None,
        basti_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''The properties for the bastion access security group.

        :param vpc: The VPC in which to create the security group.
        :param allow_all_ipv6_outbound: Whether to allow all outbound ipv6 traffic by default. If this is set to true, there will only be a single egress rule which allows all outbound ipv6 traffic. If this is set to false, no outbound traffic will be allowed by default and all egress ipv6 traffic must be explicitly authorized. To allow all ipv4 traffic use allowAllOutbound Default: false
        :param allow_all_outbound: Whether to allow all outbound traffic by default. If this is set to true, there will only be a single egress rule which allows all outbound traffic. If this is set to false, no outbound traffic will be allowed by default and all egress traffic must be explicitly authorized. To allow all ipv6 traffic use allowAllIpv6Outbound Default: true
        :param description: A description of the security group. Default: The default name will be the construct's CDK path.
        :param disable_inline_rules: Whether to disable inline ingress and egress rule optimization. If this is set to true, ingress and egress rules will not be declared under the SecurityGroup in cloudformation, but will be separate elements. Inlining rules is an optimization for producing smaller stack templates. Sometimes this is not desirable, for example when security group access is managed via tags. The default value can be overriden globally by setting the context variable '@aws-cdk/aws-ec2.securityGroupDisableInlineRules'. Default: false
        :param security_group_name: The name of the security group. For valid values, see the GroupName parameter of the CreateSecurityGroup action in the Amazon EC2 API Reference. It is not recommended to use an explicit group name. Default: If you don't specify a GroupName, AWS CloudFormation generates a unique physical ID and uses that ID for the group name.
        :param basti_id: Basti ID. This ID is used as a suffix for the name, it is not the ID of the basti instance. Default: - A 8-character pseudo-random string
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80155f9d79726f26f5e96ec5e5bf13d3e3dc94dac96daf7a46bfc6f5da964648)
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
            check_type(argname="argument allow_all_ipv6_outbound", value=allow_all_ipv6_outbound, expected_type=type_hints["allow_all_ipv6_outbound"])
            check_type(argname="argument allow_all_outbound", value=allow_all_outbound, expected_type=type_hints["allow_all_outbound"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument disable_inline_rules", value=disable_inline_rules, expected_type=type_hints["disable_inline_rules"])
            check_type(argname="argument security_group_name", value=security_group_name, expected_type=type_hints["security_group_name"])
            check_type(argname="argument basti_id", value=basti_id, expected_type=type_hints["basti_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "vpc": vpc,
        }
        if allow_all_ipv6_outbound is not None:
            self._values["allow_all_ipv6_outbound"] = allow_all_ipv6_outbound
        if allow_all_outbound is not None:
            self._values["allow_all_outbound"] = allow_all_outbound
        if description is not None:
            self._values["description"] = description
        if disable_inline_rules is not None:
            self._values["disable_inline_rules"] = disable_inline_rules
        if security_group_name is not None:
            self._values["security_group_name"] = security_group_name
        if basti_id is not None:
            self._values["basti_id"] = basti_id

    @builtins.property
    def vpc(self) -> _aws_cdk_aws_ec2_ceddda9d.IVpc:
        '''The VPC in which to create the security group.'''
        result = self._values.get("vpc")
        assert result is not None, "Required property 'vpc' is missing"
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.IVpc, result)

    @builtins.property
    def allow_all_ipv6_outbound(self) -> typing.Optional[builtins.bool]:
        '''Whether to allow all outbound ipv6 traffic by default.

        If this is set to true, there will only be a single egress rule which allows all
        outbound ipv6 traffic. If this is set to false, no outbound traffic will be allowed by
        default and all egress ipv6 traffic must be explicitly authorized.

        To allow all ipv4 traffic use allowAllOutbound

        :default: false
        '''
        result = self._values.get("allow_all_ipv6_outbound")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def allow_all_outbound(self) -> typing.Optional[builtins.bool]:
        '''Whether to allow all outbound traffic by default.

        If this is set to true, there will only be a single egress rule which allows all
        outbound traffic. If this is set to false, no outbound traffic will be allowed by
        default and all egress traffic must be explicitly authorized.

        To allow all ipv6 traffic use allowAllIpv6Outbound

        :default: true
        '''
        result = self._values.get("allow_all_outbound")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the security group.

        :default: The default name will be the construct's CDK path.
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def disable_inline_rules(self) -> typing.Optional[builtins.bool]:
        '''Whether to disable inline ingress and egress rule optimization.

        If this is set to true, ingress and egress rules will not be declared under the
        SecurityGroup in cloudformation, but will be separate elements.

        Inlining rules is an optimization for producing smaller stack templates. Sometimes
        this is not desirable, for example when security group access is managed via tags.

        The default value can be overriden globally by setting the context variable
        '@aws-cdk/aws-ec2.securityGroupDisableInlineRules'.

        :default: false
        '''
        result = self._values.get("disable_inline_rules")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def security_group_name(self) -> typing.Optional[builtins.str]:
        '''The name of the security group.

        For valid values, see the GroupName
        parameter of the CreateSecurityGroup action in the Amazon EC2 API
        Reference.

        It is not recommended to use an explicit group name.

        :default:

        If you don't specify a GroupName, AWS CloudFormation generates a
        unique physical ID and uses that ID for the group name.
        '''
        result = self._values.get("security_group_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def basti_id(self) -> typing.Optional[builtins.str]:
        '''Basti ID.

        This ID is used as a suffix for the name, it is not the ID of the basti
        instance.

        :default: - A 8-character pseudo-random string
        '''
        result = self._values.get("basti_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BastiAccessSecurityGroupProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="basti-cdk.BastiInstanceProps",
    jsii_struct_bases=[],
    name_mapping={
        "vpc": "vpc",
        "basti_id": "bastiId",
        "instance_type": "instanceType",
        "machine_image": "machineImage",
        "vpc_subnets": "vpcSubnets",
    },
)
class BastiInstanceProps:
    def __init__(
        self,
        *,
        vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
        basti_id: typing.Optional[builtins.str] = None,
        instance_type: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.InstanceType] = None,
        machine_image: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IMachineImage] = None,
        vpc_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''The properties for the bastion instance.

        :param vpc: The VPC to deploy the bastion instance into.
        :param basti_id: (Optional) The ID of the bastion instance. The ID will be used to identify the bastion instance. If not specified, a random ID will be generated. Default: - A 8-character pseudo-random string
        :param instance_type: (Optional) The instance type to use for the bastion instance. Default: t2.micro
        :param machine_image: (Optional) The machine image to use for the bastion instance.
        :param vpc_subnets: (Optional) The subnet selection to deploy the bastion instance into. If not specified, the default subnet selection will be used. Default: - Public subnets in the VPC
        '''
        if isinstance(vpc_subnets, dict):
            vpc_subnets = _aws_cdk_aws_ec2_ceddda9d.SubnetSelection(**vpc_subnets)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d790d9587a6020f94a791d6203069ecee283da08187ad5d31fa051a251fb8c17)
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
            check_type(argname="argument basti_id", value=basti_id, expected_type=type_hints["basti_id"])
            check_type(argname="argument instance_type", value=instance_type, expected_type=type_hints["instance_type"])
            check_type(argname="argument machine_image", value=machine_image, expected_type=type_hints["machine_image"])
            check_type(argname="argument vpc_subnets", value=vpc_subnets, expected_type=type_hints["vpc_subnets"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "vpc": vpc,
        }
        if basti_id is not None:
            self._values["basti_id"] = basti_id
        if instance_type is not None:
            self._values["instance_type"] = instance_type
        if machine_image is not None:
            self._values["machine_image"] = machine_image
        if vpc_subnets is not None:
            self._values["vpc_subnets"] = vpc_subnets

    @builtins.property
    def vpc(self) -> _aws_cdk_aws_ec2_ceddda9d.IVpc:
        '''The VPC to deploy the bastion instance into.'''
        result = self._values.get("vpc")
        assert result is not None, "Required property 'vpc' is missing"
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.IVpc, result)

    @builtins.property
    def basti_id(self) -> typing.Optional[builtins.str]:
        '''(Optional) The ID of the bastion instance.

        The ID will be used to identify
        the bastion instance. If not specified, a random ID will be generated.

        :default: - A 8-character pseudo-random string
        '''
        result = self._values.get("basti_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def instance_type(self) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.InstanceType]:
        '''(Optional) The instance type to use for the bastion instance.

        :default: t2.micro
        '''
        result = self._values.get("instance_type")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.InstanceType], result)

    @builtins.property
    def machine_image(self) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IMachineImage]:
        '''(Optional) The machine image to use for the bastion instance.'''
        result = self._values.get("machine_image")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IMachineImage], result)

    @builtins.property
    def vpc_subnets(self) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection]:
        '''(Optional) The subnet selection to deploy the bastion instance into.

        If not specified, the default subnet selection will be used.

        :default: - Public subnets in the VPC
        '''
        result = self._values.get("vpc_subnets")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BastiInstanceProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.interface(jsii_type="basti-cdk.IBastiInstance")
class IBastiInstance(typing_extensions.Protocol):
    @builtins.property
    @jsii.member(jsii_name="bastiId")
    def basti_id(self) -> builtins.str:
        '''The ID of the bastion instance.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="role")
    def role(self) -> _aws_cdk_aws_iam_ceddda9d.IRole:
        '''The bastion instance role.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="securityGroup")
    def security_group(self) -> _aws_cdk_aws_ec2_ceddda9d.ISecurityGroup:
        '''The bastion instance security group.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="vpc")
    def vpc(self) -> _aws_cdk_aws_ec2_ceddda9d.IVpc:
        '''The VPC the bastion instance is deployed into.'''
        ...


class _IBastiInstanceProxy:
    __jsii_type__: typing.ClassVar[str] = "basti-cdk.IBastiInstance"

    @builtins.property
    @jsii.member(jsii_name="bastiId")
    def basti_id(self) -> builtins.str:
        '''The ID of the bastion instance.'''
        return typing.cast(builtins.str, jsii.get(self, "bastiId"))

    @builtins.property
    @jsii.member(jsii_name="role")
    def role(self) -> _aws_cdk_aws_iam_ceddda9d.IRole:
        '''The bastion instance role.'''
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.IRole, jsii.get(self, "role"))

    @builtins.property
    @jsii.member(jsii_name="securityGroup")
    def security_group(self) -> _aws_cdk_aws_ec2_ceddda9d.ISecurityGroup:
        '''The bastion instance security group.'''
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup, jsii.get(self, "securityGroup"))

    @builtins.property
    @jsii.member(jsii_name="vpc")
    def vpc(self) -> _aws_cdk_aws_ec2_ceddda9d.IVpc:
        '''The VPC the bastion instance is deployed into.'''
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.IVpc, jsii.get(self, "vpc"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IBastiInstance).__jsii_proxy_class__ = lambda : _IBastiInstanceProxy


@jsii.implements(IBastiInstance)
class BastiInstance(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="basti-cdk.BastiInstance",
):
    '''The basti instance.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
        basti_id: typing.Optional[builtins.str] = None,
        instance_type: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.InstanceType] = None,
        machine_image: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IMachineImage] = None,
        vpc_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param vpc: The VPC to deploy the bastion instance into.
        :param basti_id: (Optional) The ID of the bastion instance. The ID will be used to identify the bastion instance. If not specified, a random ID will be generated. Default: - A 8-character pseudo-random string
        :param instance_type: (Optional) The instance type to use for the bastion instance. Default: t2.micro
        :param machine_image: (Optional) The machine image to use for the bastion instance.
        :param vpc_subnets: (Optional) The subnet selection to deploy the bastion instance into. If not specified, the default subnet selection will be used. Default: - Public subnets in the VPC
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4158f394054ae1209b1cd72557325674fee43baac5126ca6abae5e7e35b0c4b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = BastiInstanceProps(
            vpc=vpc,
            basti_id=basti_id,
            instance_type=instance_type,
            machine_image=machine_image,
            vpc_subnets=vpc_subnets,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromBastiId")
    @builtins.classmethod
    def from_basti_id(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        basti_id: builtins.str,
        vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
    ) -> IBastiInstance:
        '''Create a bastion instance from an existing Basti ID.

        :param scope: CDK construct scope.
        :param id: CDK construct ID.
        :param basti_id: The ID of the basti instance.
        :param vpc: The VPC that the bastion is deployed into.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae0feb86b982d3c8e869368ffcf99385131903782b5b5e3650e5b9879d098e34)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument basti_id", value=basti_id, expected_type=type_hints["basti_id"])
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
        return typing.cast(IBastiInstance, jsii.sinvoke(cls, "fromBastiId", [scope, id, basti_id, vpc]))

    @jsii.member(jsii_name="grantBastiCliConnect")
    def grant_basti_cli_connect(
        self,
        grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    ) -> None:
        '''Grants an IAM principal permission to connect to the bastion instance.

        Using the Basti CLI.

        :param grantee: The principal to grant permission to.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f801a712fc6f5ade326c40f89b291d3c6c5b376f582c4a0877eea1a50117b9a5)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast(None, jsii.invoke(self, "grantBastiCliConnect", [grantee]))

    @builtins.property
    @jsii.member(jsii_name="bastiId")
    def basti_id(self) -> builtins.str:
        '''The ID of the bastion instance.'''
        return typing.cast(builtins.str, jsii.get(self, "bastiId"))

    @builtins.property
    @jsii.member(jsii_name="instance")
    def instance(self) -> _aws_cdk_aws_ec2_ceddda9d.Instance:
        '''The bastion instance.'''
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.Instance, jsii.get(self, "instance"))

    @builtins.property
    @jsii.member(jsii_name="role")
    def role(self) -> _aws_cdk_aws_iam_ceddda9d.IRole:
        '''The bastion instance role.'''
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.IRole, jsii.get(self, "role"))

    @builtins.property
    @jsii.member(jsii_name="securityGroup")
    def security_group(self) -> _aws_cdk_aws_ec2_ceddda9d.ISecurityGroup:
        '''The bastion instance security group.'''
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup, jsii.get(self, "securityGroup"))

    @builtins.property
    @jsii.member(jsii_name="vpc")
    def vpc(self) -> _aws_cdk_aws_ec2_ceddda9d.IVpc:
        '''The VPC the bastion instance is deployed into.'''
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.IVpc, jsii.get(self, "vpc"))


__all__ = [
    "BastiAccessSecurityGroup",
    "BastiAccessSecurityGroupProps",
    "BastiInstance",
    "BastiInstanceProps",
    "IBastiInstance",
]

publication.publish()

def _typecheckingstub__01948589ed1a60919700df630bf7069a9d8c730904dc0053525f1ca445fc0678(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    basti_id: typing.Optional[builtins.str] = None,
    vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
    allow_all_ipv6_outbound: typing.Optional[builtins.bool] = None,
    allow_all_outbound: typing.Optional[builtins.bool] = None,
    description: typing.Optional[builtins.str] = None,
    disable_inline_rules: typing.Optional[builtins.bool] = None,
    security_group_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d033d471ed35bb19d7d2268c0a4a86abc74b88e32fdb3c7330adb7ad118b4dd(
    basti_instance: IBastiInstance,
    port: _aws_cdk_aws_ec2_ceddda9d.Port,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80155f9d79726f26f5e96ec5e5bf13d3e3dc94dac96daf7a46bfc6f5da964648(
    *,
    vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
    allow_all_ipv6_outbound: typing.Optional[builtins.bool] = None,
    allow_all_outbound: typing.Optional[builtins.bool] = None,
    description: typing.Optional[builtins.str] = None,
    disable_inline_rules: typing.Optional[builtins.bool] = None,
    security_group_name: typing.Optional[builtins.str] = None,
    basti_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d790d9587a6020f94a791d6203069ecee283da08187ad5d31fa051a251fb8c17(
    *,
    vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
    basti_id: typing.Optional[builtins.str] = None,
    instance_type: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.InstanceType] = None,
    machine_image: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IMachineImage] = None,
    vpc_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4158f394054ae1209b1cd72557325674fee43baac5126ca6abae5e7e35b0c4b(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
    basti_id: typing.Optional[builtins.str] = None,
    instance_type: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.InstanceType] = None,
    machine_image: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IMachineImage] = None,
    vpc_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae0feb86b982d3c8e869368ffcf99385131903782b5b5e3650e5b9879d098e34(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    basti_id: builtins.str,
    vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f801a712fc6f5ade326c40f89b291d3c6c5b376f582c4a0877eea1a50117b9a5(
    grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
) -> None:
    """Type checking stubs"""
    pass
