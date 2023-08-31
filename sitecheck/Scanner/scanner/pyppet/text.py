"""
    Text Package for Pyppet
    Selectors can be long and clutter up functions
"""
import os


class Amp_text:
    """
        Text values for use in Amp-specific Events

        type: (str)
        username, password, label, logincss, pwcss,
        urlstring, loginbutton, planview,
        csspath, title, sensor
    """
    username = os.environ.get('SCANNER_AMPUSER')
    password = os.environ.get('SCANNER_AMPPASS')
    label = ['3', '4']
    logincss = '#s_text_login_name'
    pwcss = '#s_password_login_password'
    urlstring = '.geo-instruments.com/index.php'
    loginbutton = 'body > div > form > input.button'
    planview = '?s_cat=project&i_project=17&i_planview='


class Qv_text:
    """
            Text values for use in QV-specific Events

            type: (str)
            username, password, logincss, pwcss, urlstring,
            loginbutton, projects, proj_pre, proj_post, views,
            thumb, scrollbar, scrollbar2, hoverbox, searchbar
        """
    username = os.environ.get('SCANNER_QVUSER')
    password = os.environ.get('SCANNER_QVPASS')
    date = os.environ['Nowdate']
    logincss = '#user'
    pwcss = '#pass'
    loginbutton = '#login > form > button'
    projects = '#menuProjects > a > i'
    proj_pre = 'div#projectList div:nth-child('
    proj_post = ') > div.panelRowTxt2'
    views = 'li#menuViews p'
    thumb = '#thumb'
    scrollbar = 'body > div.wrapper > div.sidePanel.ui-resizable > img'
    scrollbar2 = 'body > div.wrapper > div.sideP' \
                 'anel.ui-resizable > img'
    hoverbox = "#hoverBox"
    searchbar = '.wrapper #projectSearchInput'
    graphs = '#menuGraphs > a > p'
    journal = '#menuJournal > a > p'
    addbutton = "# quickAdd"
