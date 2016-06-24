# Spring Config Decorator

This is a [decorator](https://github.com/cf-platform-eng/meta-buildpack/blob/master/README.md#decorators) buildpack
for Cloud Foundry that provides integration with the Spring Cloud Config server *for any programming
lanugage* supported by the platform, and requiring *zero application code changes*.

When this decorator (and the [meta-buildpack](https://github.com/cf-platform-eng/meta-buildpack))
is present in your Cloud Foundry deployment, all you will have to do to inject
centrally managed configuration into your applications is bind the application to your Spring Cloud
Config Server instance. Your application will then automatically receive the properties configured
in that server in its environment.

