# Spring Config Decorator

> <b>NOTE: Meta-buildback is being deprecated</b><br/>
> Changes to the core CloudFoundry lifecycle process are making it hard to guarantee
> on-going compatibility with meta-buildpack and decorators. Some of the use cases for
> decorators can now be solved by leveraging the new
> [supply buildpack](https://docs.cloudfoundry.org/buildpacks/understand-buildpacks.html#supply-script)
> functionality. An updated example using that new mechanism can be found here:
>
> [New Spring Config](https://github.com/cf-platform-eng/spring-config-injection)

This is a [decorator](https://github.com/cf-platform-eng/meta-buildpack/blob/master/README.md#decorators) buildpack
for Cloud Foundry that provides integration with the Spring Cloud Config server *for any programming
language* supported by the platform, and requiring *zero application code changes*.

When this decorator (and the [meta-buildpack](https://github.com/cf-platform-eng/meta-buildpack))
is present in your Cloud Foundry deployment, all you will have to do to inject
centrally managed configuration into your applications is bind the application to your Spring Cloud
Config Server instance. Your application will then automatically receive the properties configured
in that server in its environment.

