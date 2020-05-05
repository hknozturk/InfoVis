global indexString
indexString = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>US FARS Visualisation</title>
        {%favicon%}
        {%css%}
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''
