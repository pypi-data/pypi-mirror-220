import json

import click
import structlog

from hukudo.gitlab.api import Gitlab
from hukudo.gitlab.jobs import get_duration, JobDurationParseError

logger = structlog.get_logger()

pass_gitlab = click.make_pass_decorator(Gitlab)


@click.group()
@click.option('--name')
@click.pass_context
def gitlab(ctx, name):
    ctx.obj = Gitlab.from_ini(name)
    log = logger.bind(instance=ctx.obj)
    log.debug('instantiated')


@gitlab.command()
@pass_gitlab
def version(gitlab: Gitlab):
    click.echo(gitlab.version())


@gitlab.command()
@click.argument('project')
@pass_gitlab
def jobs(gitlab: Gitlab, project):
    for job in gitlab.jobs_of_project(project):
        try:
            job.attributes['duration'] = get_duration(job.attributes)
            print(json.dumps(job.attributes))
        except JobDurationParseError:
            pass
