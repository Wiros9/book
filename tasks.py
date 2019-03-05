from atelier.invlib import setup_from_tasks
ns = setup_from_tasks(
    globals(), 'lino_book',
    # tolerate_sphinx_warnings=True,
    blogref_url="http://luc.lino-framework.org",
    revision_control_system='git',
    # help_texts_source='docs',
    # help_texts_module='lino_xl.lib.xl',
    cleanable_files=[
        'docs/rss_entry_fragments/*',
        'docs/api/lino.*',
        'docs/api/lino_xl.*',
        'docs/api/lino_noi.*',
        'docs/api/lino_cosi.*',
        'docs/api/lino_avanti.*',
        'docs/api/lino_vilma.*',
        'docs/api/lino_tera.*',
        'docs/api/lino_care.*',
        'docs/api/lino_voga.*',
        'docs/api/lino_amici.*',
        'docs/api/lino_welfare.*',
        'docs/api/lino_welcht.*',
        'docs/api/lino_book.*'],
    demo_projects=[
        'lino_book.projects.gerd',
        # 'lino_book.projects.mathieu',
        'lino_book.projects.roger',
        'lino_book.projects.edmund',
        'lino_book.projects.combo',
        'lino_book.projects.watch',
        'lino_book.projects.watch2',
        'lino_book.projects.workflows',
        'lino_book.projects.docs',
        'lino_book.projects.belref',
        'lino_book.projects.polly',
        'lino_book.projects.events',
        'lino_book.projects.max',
        'lino_book.projects.i18n',
        'lino_book.projects.lets1',
        'lino_book.projects.lets2',
        'lino_book.projects.min1',
        'lino_book.projects.min2',
        'lino_book.projects.min3',
        'lino_book.projects.min9',
        'lino_book.projects.mti',
        'lino_book.projects.nomti',
        'lino_book.projects.cms',
        'lino_book.projects.apc',
        'lino_book.projects.pierre',
        'lino_book.projects.cosi_ee',
        'lino_book.projects.chatter',
        'lino_book.projects.team',
        'lino_book.projects.adg',
        'lino_book.projects.anna',
        'lino_book.projects.liina',
        'lino_book.projects.lydia',
        'lino_book.projects.gfktest',
        'lino_book.projects.actions',
        'lino_book.projects.actors',
        'lino_book.projects.tables',
        'lino_book.projects.vtables',
        'lino_book.projects.integer_pk',
        'lino_book.projects.float2decimal',
        'lino_book.projects.myroles',
        'lino_book.projects.mldbc',
        'lino_book.projects.human',
        'lino_book.projects.de_BE',
        'lino_book.projects.auto_create',
        'lino_book.projects.addrloc',
        'lino_openui5.projects.teamUi5',
        'lino_openui5.projects.lydiaUi5',
        
        # 'lino_book/projects/diamond',
        # 'lino_book/projects/diamond2',
        # 'lino_book/projects/polls',
        # 'lino_book/projects/polls2',
        # 'lino_book/projects/sendchanges',
        # 'lino_book/projects/pisa',
    ])
