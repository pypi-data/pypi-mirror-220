'''
# AWS FSx Life Cycle Status Monitor

The documentation is available [here](https://stefanfreitag.github.io/AWS-FSx-Lifecycle-Status-Monitor/).

## How to run

### Tests

* Execute the unit tests under `./test`

  ```shell
  yarn test
  ```
* Execute integration tests under `.integ-tests`

  ```shell
  yarn integ-runner --directory ./integ-tests  --update-on-failed --parallel-regions eu-central-1
  ```
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

import aws_cdk.aws_events as _aws_cdk_aws_events_ceddda9d
import aws_cdk.aws_iam as _aws_cdk_aws_iam_ceddda9d
import aws_cdk.aws_lambda as _aws_cdk_aws_lambda_ceddda9d
import aws_cdk.aws_sns as _aws_cdk_aws_sns_ceddda9d
import constructs as _constructs_77d1e7e8


class FsxLifecycleStatusMonitor(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws_fsx_lifecycle_status_monitor.FsxLifecycleStatusMonitor",
):
    '''
    :stability: experimental
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        schedule: typing.Optional[_aws_cdk_aws_events_ceddda9d.Schedule] = None,
    ) -> None:
        '''(experimental) Creates an instance of FsxLifecycleStatusMonitor.

        :param scope: - parent construct.
        :param id: - unique id.
        :param schedule: (experimental) The schedule for the FSx Lifecycle Status Monitor.

        :stability: experimental
        :memberof: FsxLifecycleStatusMonitor - class instance
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0bea38a9f9d3a7ccb22620e56835a7b5cbf0ec89beae2d61e0ea183098f5416c)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = FsxLifecycleStatusMonitorProps(schedule=schedule)

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="createIamPolicy")
    def create_iam_policy(self) -> _aws_cdk_aws_iam_ceddda9d.Policy:
        '''
        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.Policy, jsii.invoke(self, "createIamPolicy", []))

    @jsii.member(jsii_name="createLambdaFunction")
    def create_lambda_function(self) -> _aws_cdk_aws_lambda_ceddda9d.Function:
        '''
        :return: {lambda.Function}

        :stability: experimental
        :memberof: FsxLifecycleStatusMonitor
        '''
        return typing.cast(_aws_cdk_aws_lambda_ceddda9d.Function, jsii.invoke(self, "createLambdaFunction", []))

    @jsii.member(jsii_name="createSNSTopic")
    def create_sns_topic(self) -> _aws_cdk_aws_sns_ceddda9d.Topic:
        '''(experimental) Topic linked to the Lambda function.

        :return: {sns.Topic} - sns topic

        :stability: experimental
        :memberof: FsxLifecycleStatusMonitor - class instance
        '''
        return typing.cast(_aws_cdk_aws_sns_ceddda9d.Topic, jsii.invoke(self, "createSNSTopic", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="DEFAULT_SCHEDULE")
    def DEFAULT_SCHEDULE(cls) -> _aws_cdk_aws_events_ceddda9d.Schedule:
        '''
        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_events_ceddda9d.Schedule, jsii.sget(cls, "DEFAULT_SCHEDULE"))

    @builtins.property
    @jsii.member(jsii_name="fn")
    def fn(self) -> _aws_cdk_aws_lambda_ceddda9d.Function:
        '''
        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_lambda_ceddda9d.Function, jsii.get(self, "fn"))

    @fn.setter
    def fn(self, value: _aws_cdk_aws_lambda_ceddda9d.Function) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5b694d5a48779fe78e91dc649a27c8dd309970cb1029cc68a6db3312ca2dd0a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fn", value)

    @builtins.property
    @jsii.member(jsii_name="policy")
    def policy(self) -> _aws_cdk_aws_iam_ceddda9d.Policy:
        '''
        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.Policy, jsii.get(self, "policy"))

    @policy.setter
    def policy(self, value: _aws_cdk_aws_iam_ceddda9d.Policy) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0817232f0cba7b0115bdd3fefb7ac5b03061a704e15a06fa2d7fb3439519644)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "policy", value)

    @builtins.property
    @jsii.member(jsii_name="rule")
    def rule(self) -> _aws_cdk_aws_events_ceddda9d.Rule:
        '''
        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_events_ceddda9d.Rule, jsii.get(self, "rule"))

    @rule.setter
    def rule(self, value: _aws_cdk_aws_events_ceddda9d.Rule) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1307118b507bd5fe4ac4e20cfeb79870f16bba9b44d219f4a6506f94baf6b71e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rule", value)

    @builtins.property
    @jsii.member(jsii_name="topic")
    def topic(self) -> _aws_cdk_aws_sns_ceddda9d.Topic:
        '''
        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_sns_ceddda9d.Topic, jsii.get(self, "topic"))

    @topic.setter
    def topic(self, value: _aws_cdk_aws_sns_ceddda9d.Topic) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5fdedb79384d0423e054048b7b549d7ea785a9973c1ddc97237c3d96599983dd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "topic", value)


@jsii.data_type(
    jsii_type="aws_fsx_lifecycle_status_monitor.FsxLifecycleStatusMonitorProps",
    jsii_struct_bases=[],
    name_mapping={"schedule": "schedule"},
)
class FsxLifecycleStatusMonitorProps:
    def __init__(
        self,
        *,
        schedule: typing.Optional[_aws_cdk_aws_events_ceddda9d.Schedule] = None,
    ) -> None:
        '''(experimental) Properties for the FSx Lifecycle Status Monitor.

        :param schedule: (experimental) The schedule for the FSx Lifecycle Status Monitor.

        :stability: experimental
        :export: true
        :interface: FsxLifecycleStatusMonitorProps
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be461e59cf3d96e472a6b442ffba1268fe66c6514c192dd611bc338a68ef6483)
            check_type(argname="argument schedule", value=schedule, expected_type=type_hints["schedule"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if schedule is not None:
            self._values["schedule"] = schedule

    @builtins.property
    def schedule(self) -> typing.Optional[_aws_cdk_aws_events_ceddda9d.Schedule]:
        '''(experimental) The schedule for the FSx Lifecycle Status Monitor.

        :stability: experimental
        :memberof: FsxLifecycleStatusMonitorProps
        :type: {events.Schedule}

        Example::

            "events.Schedule.cron({ minute: '0/10', hour: '*', day: '*', month: '*', year: '*' })"
        '''
        result = self._values.get("schedule")
        return typing.cast(typing.Optional[_aws_cdk_aws_events_ceddda9d.Schedule], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FsxLifecycleStatusMonitorProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "FsxLifecycleStatusMonitor",
    "FsxLifecycleStatusMonitorProps",
]

publication.publish()

def _typecheckingstub__0bea38a9f9d3a7ccb22620e56835a7b5cbf0ec89beae2d61e0ea183098f5416c(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    schedule: typing.Optional[_aws_cdk_aws_events_ceddda9d.Schedule] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5b694d5a48779fe78e91dc649a27c8dd309970cb1029cc68a6db3312ca2dd0a(
    value: _aws_cdk_aws_lambda_ceddda9d.Function,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0817232f0cba7b0115bdd3fefb7ac5b03061a704e15a06fa2d7fb3439519644(
    value: _aws_cdk_aws_iam_ceddda9d.Policy,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1307118b507bd5fe4ac4e20cfeb79870f16bba9b44d219f4a6506f94baf6b71e(
    value: _aws_cdk_aws_events_ceddda9d.Rule,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5fdedb79384d0423e054048b7b549d7ea785a9973c1ddc97237c3d96599983dd(
    value: _aws_cdk_aws_sns_ceddda9d.Topic,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be461e59cf3d96e472a6b442ffba1268fe66c6514c192dd611bc338a68ef6483(
    *,
    schedule: typing.Optional[_aws_cdk_aws_events_ceddda9d.Schedule] = None,
) -> None:
    """Type checking stubs"""
    pass
