from types import SimpleNamespace
from aws_cdk import (
    core,
    aws_ec2 as ec2,
    aws_ecs as ecs,
    aws_ecs_patterns as ecs_patterns,
    aws_rds as rds,
    # aws_elasticloadbalancingv2 as elb,
    aws_servicediscovery as servicediscovery,
    aws_logs as logs,
)


class OsmStack(core.Stack):
    def __init__(
        self, scope: core.Construct, id: str, config: SimpleNamespace, **kwargs
    ) -> None:
        super().__init__(scope, id, **kwargs)

        vpc = ec2.Vpc(
            self, f"{config.env_id}Vpc", max_azs=3, cidr=config.cidr_block
        )

        namespace = servicediscovery.PrivateDnsNamespace(
            self,
            f"{config.env_id}Namespace",
            name=config.private_dns_name,
            vpc=vpc
        )

        log_group = logs.LogGroup(
            self,
            f"{config.env_id}LogGroup",
            log_group_name=f"{config.env_id}SecureMaps"
        )

        cluster = ecs.Cluster(
            self, f"{config.env_id}Cluster", vpc=vpc, container_insights=True
        )

        #
        # Databases
        #
        postgres = rds.DatabaseInstance(
            self,
            f"{config.env_id}OsmDb",
            engine=rds.DatabaseInstanceEngine.POSTGRES,
            instance_type=config.rds.instance_type,
            # instance_identifier=f"{config.env_id}-osm-db",
            vpc=vpc,
            deletion_protection=True,
            multi_az=config.rds.multi_az,
        )

        #
        # Apps
        #
        osm_web = ecs_patterns.ApplicationLoadBalancedFargateService(
            self,
            f"{config.env_id}OsmWeb",
            cluster=cluster,
            # domain_zone=domain_zone,
            # domain_name=domain_name,
            # certificate=cert, # TODO need this for HTTPS
            # load_balancer=lb,
            # public_load_balancer=True,
            # protocol=elb.ApplicationProtocol.HTTP,
            redirect_http=False,  # TODO change once we have a certificate.
            cpu=config.osm_web.cpu,
            memory_limit_mib=config.osm_web.memory,
            desired_count=config.osm_web.count,
            cloud_map_options=ecs.CloudMapOptions(
                cloud_map_namespace=namespace, name="osm-web"
            ),
            task_image_options=ecs_patterns.
            ApplicationLoadBalancedTaskImageOptions(
                image=ecs.ContainerImage.from_asset("../osm-custom"),
                container_port=3000,
                # environment={
                #     "ENVIRONMENT": stack_name,
                # },
                secrets={
                    "POSTGRES_CREDENTIALS":
                        ecs.Secret.from_secrets_manager(postgres.secret)
                },
                enable_logging=True,
                log_driver=ecs.LogDrivers.aws_logs(
                    stream_prefix=f"{config.env_id}OsmWeb", log_group=log_group
                ),
            ),
        )
        postgres.connections.allow_default_port_from(osm_web.service)
