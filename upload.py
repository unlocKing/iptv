#!/usr/bin/env python
# -*- coding: utf-8 -*-
try:
    from configparser import ConfigParser
except ImportError:
    # python 2.7
    from ConfigParser import ConfigParser

from ftplib import FTP


class UPLOAD(object):
    """FTP upload script.

       IPTV M3U Playlist Generator for Livecli Proxy
       https://github.com/livecli/iptv
    """

    def __init__(self):
        self.run()

    def read_config(self):
        print("[debug] read config")
        self.config_data = {
            "filename": "playlist.m3u",
        }

        self.config_ftp = {
            "username": "",
            "password": "",
            "host": "",
            "path": ""
        }

        config = ConfigParser()
        config.read(["defaults.cfg"])
        if "iptv" in config.sections():
            for key in config["iptv"]:
                self.config_data[key] = config["iptv"][key]

        if "upload" in config.sections():
            for key in config["upload"]:
                self.config_ftp[key] = config["upload"][key]

    def upload_playlist(self):
        print("[debug] upload playlist")

        error = False
        for x in ("username", "password", "host", "path"):
            if not self.config_ftp.get(x):
                print("[error] missing {0}".format(x))
                error = True

        if error is True:
            return

        with FTP(self.config_ftp.get("host")) as ftp:
            ftp.login(
                user=self.config_ftp.get("username"),
                passwd=self.config_ftp.get("password")
            )
            print("[debug] {0}".format(ftp.getwelcome()))
            print("[debug] current directory: {0}".format(ftp.pwd()))
            ftp.cwd(self.config_ftp.get("path"))
            print("[debug] upload directory:  {0}".format(ftp.pwd()))
            print("[debug] uploading {0}".format(self.config_data.get("filename")))
            myfile = open(self.config_data.get("filename"), "rb")
            ftp.storbinary("STOR {0}".format(str(self.config_data.get("filename"))), myfile)
            myfile.close()
            ftp.quit()
            print("[debug] Done")

    def run(self):
        self.read_config()
        self.upload_playlist()


if __name__ == "__main__":
    UPLOAD()
