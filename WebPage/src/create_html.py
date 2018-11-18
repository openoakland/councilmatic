#
# Read a template file and then write it main file


def create_html(url_open, fx):
    in_file = open(url_open, 'r')
    page = in_file.read()
    fx.write(page)
    in_file.close()
    return

