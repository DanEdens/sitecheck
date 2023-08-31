"""
    Geo-Instruments
    Sitecheck scanner
    Project handler Package for scanner
"""
import logging
import os

from . import adaptivecards
from . import config
from . import options
from . import pyppet

logger = logging.getLogger('projecthandler')


async def run_controller(project):
    """

        If --project is default, the "skip" value will be checked,
        Will than Scan the project or pass

        If --project is other than default. The first check will filter
        out the other projects silently, only running the given value.
        Cancels run if project.skip is true


    :returns: none

    """
    job = Project_runner(project)

    # Check for Default value 'All'
    if options.Project != 'All':
        # If not 'All' filter out everything except --project
        if options.Project == 'force':
            async with job:
                await job.project_site_handler()
        elif job.title == options.Project:
            async with job:
                await job.project_site_handler()
        else:
            return 0
    else:
        if job.project.skip == 'true':
            logger.info(f'Skipping project: {job.title}')
        else:
            async with job:
                await job.project_site_handler()


class Project_runner:
    """Project Run Object

    """

    def __init__(self, project_title):
        self.title = project_title
        self.project = config.tuple_from_section_config(project_title)
        self.url = f'https://{self.project.name}.geo-instruments.com'

    async def __aenter__(self):
        await pyppet.launch(self)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        try:
            if not os.environ['Repl']:
                await self.browser.close()
            else:
                pass
                # await self.browser.disconnect()
        except IOError:
            pass

    async def project_skip_handler(self):
        """
        Cancels run if project.skip is true

        If --project is other than default. The first check will filter
        out the other projects silently, only running the given value.

        If --project is default, the "skip" value will be checked, passing
        if true, or scanning the project is false.

        :return: Exit code
        :rtype: int
        """
        logger.debug(f'options.project: {options.Project}\n title: '
                     f'{self.title}\n'
                     f'skip: {self.project.skip}')
        if options.Project != 'All':
            if self.title == options.Project:
                run_complete: bool = await self.project_site_handler()
            else:
                return 0
        else:
            if self.project.skip == 'true':
                return 0
            else:
                run_complete: bool = await self.project_site_handler()

        # After a successful run, Set project skip = true
        if run_complete:
            config.edit_config_option(self.title, 'skip', 'true')
        return 0

    async def project_site_handler(self):
        """
        Checks if a project is housed on Amp, Qv, and/or Truelook.
        """
        logger.info(f"{self.project.name} scan for {os.environ['filedate']}")
        logger.debug(f'Project:    {self.project.name}')
        logger.debug(f'Has Site:   {self.project.site}')
        logger.debug(f'Plan array: {self.project.planarray}\n')

        if self.project.site == 'amp':
            await pyppet.amp_runner(self)
        elif self.project.site == 'qv':
            await pyppet.qv_runner(self)
        elif self.project.site == 'truelook':
            return str('In Development')

        path_to_temp = await adaptivecards.generator(self.project)
        logger.debug(path_to_temp)
        return path_to_temp
