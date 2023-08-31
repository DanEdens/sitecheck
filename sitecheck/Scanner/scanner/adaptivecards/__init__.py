"""
    Init file for adaptivecards

    TODO: move imports to this location,
    TODO: to allow use as a stand alone module
"""
# __name__ = 'adaptivecards'

from .generator import Generator


async def generator(project):
    """ Entry point for Adaptive card Generator """
    staged_file = Generator(project)
    return staged_file.compile_data()
