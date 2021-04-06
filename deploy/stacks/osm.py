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
    aws_efs as efs
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

        file_system = efs.FileSystem(
            self,
            f"{config.env_id}Efs",
            vpc=vpc
        )

        # log_group = logs.LogGroup(
        #     self,
        #     f"{config.env_id}LogGroup",
        #     log_group_name=f"{config.env_id}SecureMaps"
        # )

        cluster = ecs.Cluster(
            self, f"{config.env_id}Cluster", vpc=vpc, container_insights=True
        )

        #
        # Databases
        #
        postgres = rds.DatabaseInstance(
            self,
            f"{config.env_id}OsmDb",
            engine=rds.DatabaseInstanceEngine.postgres(
                version=rds.PostgresEngineVersion.VER_11_9
            ),
            instance_type=config.rds.instance_type,
            # instance_identifier=f"{config.env_id}-osm-db",
            vpc=vpc,
            # deletion_protection=True,
            multi_az=config.rds.multi_az
        )

        #
        # Apps
        #
        osm_web_task_def = ecs.FargateTaskDefinition(
            self,
            f"{config.env_id}OsmWebTaskDef",
            cpu=config.osm_web.cpu,
            memory_limit_mib=config.osm_web.memory,
            volumes=[
                ecs.Volume(
                    name=f"{config.env_id}OsmWebService",
                    efs_volume_configuration=ecs.EfsVolumeConfiguration(
                        file_system_id=file_system.file_system_id,
                        root_directory="/osm-webapp"
                    )
                )
            ]
        )
        osm_web_task_def.add_container(
            f"{config.env_id}OsmWebCont",
            image=ecs.ContainerImage.from_asset("../osm-custom"),
            cpu=config.osm_web.cpu,
            memory_limit_mib=config.osm_web.memory,
            port_mappings=[
                ecs.PortMapping(container_port=3000)
            ],
            environment={
                "PGHOST": postgres.db_instance_endpoint_address,
                "PGDATABASE": "openstreetmap"
            },
            secrets={
                "PGPASSWORD":
                    ecs.Secret.from_secrets_manager(postgres.secret, field="password"),
                "PGUSER":
                    ecs.Secret.from_secrets_manager(postgres.secret, field="username")
            },
        )

        osm_web = ecs_patterns.ApplicationLoadBalancedFargateService(
            self,
            f"{config.env_id}OsmWeb",
            cluster=cluster,
            # domain_zone=domain_zone,
            # domain_name=domain_name,
            # certificate=cert, # TODO need this for HTTPS
            redirect_http=False,  # TODO change once we have a certificate.
            cpu=config.osm_web.cpu,
            memory_limit_mib=config.osm_web.memory,
            desired_count=config.osm_web.count,
            cloud_map_options=ecs.CloudMapOptions(
                cloud_map_namespace=namespace, name="osm-web"
            ),
            task_definition=osm_web_task_def,
            # task_image_options=ecs_patterns.
            # ApplicationLoadBalancedTaskImageOptions(
            #     image=ecs.ContainerImage.from_asset("../osm-custom"),
            #     container_port=3000,
            #     environment={
            #         "PGHOST": postgres.db_instance_endpoint_address,
            #         "PGDATABASE": "openstreetmap"
            #     },
            #     secrets={
            #         "PGPASSWORD":
            #             ecs.Secret.from_secrets_manager(postgres.secret, field="password"),
            #         "PGUSER":
            #             ecs.Secret.from_secrets_manager(postgres.secret, field="username")
            #     },
            #     enable_logging=True,
            #     log_driver=ecs.LogDrivers.aws_logs(
            #         stream_prefix=f"{config.env_id}OsmWeb", log_group=log_group
            #     ),
            # ),
        )

        postgres.connections.allow_default_port_from(osm_web.service)
