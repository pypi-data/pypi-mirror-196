def Web(URL):
    from colorama import Fore, Style, init
    import requests
    init()

    Pages = ["robots.txt", "search/", "admin/", "login/", "sitemap.xml",
    "sitemap2.xml", "config.php", "wp-login.php", "log.txt", "update.php",
    "INSTALL.pgsql.txt","user/login/","INSTALL.txt", "profiles/", "scripts/",
    "LICENSE.txt", "CHANGELOG.txt", "thems/", "includes/", "misc/", "user/logout/",
    "user/register/", "cron.php", "filter/tips/", "comment/reply/", "xmlrpc.php",
    "moduls/", "install.php", "MAINTAINERS.txt", "user/password/", "node/add/",
    "INSTALL.sqlite.txt", "UPGRADE.txt", "INSTALL.mysql.txt"]

    if "http" in URL:
        pass

    else:
        URL = "https://"+URL+"/"

    for Site in Pages:
        Add = URL + Site
        Req = requests.get(Add)
        if Req.status_code == 200:
            print(Fore.GREEN + "[+] Page Found > > > " + Add)
        else:
            print(Fore.RED + "[-] Page Not Found > > > " + Add)