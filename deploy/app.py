#!/usr/bin/env python3
import os
from aws_cdk import core

from config import EnvConfig
from stacks.osm import OsmStack


app = core.App()


OsmStack(
    app, 
    f"{EnvConfig.env_id}-aafc-ingest",
    config=EnvConfig,
    env=EnvConfig.env,
)


app.synth()