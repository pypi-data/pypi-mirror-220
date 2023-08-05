# AWS FSx Life Cycle Status Monitor

Monitors the health of Amazon FSx file systems by configuring
notifications on file system status changes. It helps to
quickly detect and take action if your file systems aren’t healthy.

This solution is based on this [post](https://aws.amazon.com/de/blogs/storage/monitoring-the-health-of-amazon-fsx-file-systems-using-amazon-eventbridge-and-aws-lambda/) in the AWS Storage Blog.

## How to run

### Tests

```shell
yarn test
```

### Integration tests

```shell
yarn integ-runner --directory ./integ-tests  --update-on-failed --parallel-regions eu-central-1
```

## Links

* [Amazon FSx file system status](https://docs.aws.amazon.com/fsx/latest/WindowsGuide/file-system-lifecycle-states.html)
* [Monitoring the health of Amazon FSx file systems using Amazon EventBridge and AWS Lambda](https://aws.amazon.com/de/blogs/storage/monitoring-the-health-of-amazon-fsx-file-systems-using-amazon-eventbridge-and-aws-lambda/)
