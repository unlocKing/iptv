#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import logging
import os.path
import platform
import sys

from codecs import open
from glob import glob

from configparser import ConfigParser
from urllib.parse import quote_plus
from urllib.parse import urlencode

FORMAT = "[%(name)s][%(levelname)s] %(message)s"
logging.basicConfig(format=FORMAT)
log = logging.getLogger("run")
log.setLevel(logging.DEBUG)

try:
    from data import mydata
except ModuleNotFoundError:
    log.error("Missing data.py file")
except Exception:
    log.debug("No mydata.py")
    pass


def log_current_versions():
    """Show current installed versions"""
    # MAC OS X
    if sys.platform == "darwin":
        os_version = "macOS {0}".format(platform.mac_ver()[0])
    # Windows
    elif sys.platform.startswith("win"):
        os_version = "{0} {1}".format(platform.system(), platform.release())
    # linux / other
    else:
        os_version = platform.platform()

    log.debug("OS:     {0}".format(os_version))
    log.debug("Python: {0}".format(platform.python_version()))


def percentage(a, b):
    return int(100 * float(a) / float(b))


class IPTV(object):
    """IPTV M3U Playlist Generator for LiveProxy
       https://github.com/back-to/iptv
    """

    def __init__(self):
        log_current_versions()
        self.data = []

        try:
            self.data += mydata
            log.debug("Found mydata.py")
        except NameError:
            pass

        # XXX make this changeable with the configfile
        streams_dirs = ["private"]
        error_count = []
        for streams_dir in streams_dirs:
            item_count = 0
            if os.path.isdir(streams_dir):
                _files = sorted(glob(os.path.join(streams_dir, "**", "*.json"),
                                recursive=True))
                _files_len = len(_files)
                log.debug("Found {0} files in {1}".format(_files_len,
                                                          streams_dir))
                for _file in _files:
                    item_count += 1
                    log.info("{0}% - {1}".format(
                        percentage(item_count, _files_len), _file))
                    with open(_file) as fd:
                        try:
                            self.data += [json.load(fd)]
                        except json.decoder.JSONDecodeError:
                            error_count += [_file]
                            log.error("Invalid JSON for {0}".format(_file))

        if error_count:
            raise Exception("Invalid JSON files: {0} - {1}".format(len(error_count), ', '.join(error_count)))
        else:
            log.debug("All JSON files are valid.")

        self.run()

    def sort_priority_name(self, item):
        return (int(item["priority"]), item["channel_data"][0]["name"])

    def sort_name(self, item):
        return (item["name"])

    def read_config(self):
        self.config_data = {
            "filename": "playlist.m3u",
            "host": "127.0.0.1",
            "port": "53422",
            "logopath": ""
        }

        config = ConfigParser()
        config.read(["defaults.cfg"])
        if "iptv" in config.sections():
            for key in config["iptv"]:
                self.config_data[key] = config["iptv"][key]

    def sort_data(self):
        """ sort json data
            - priority
            - name
        """
        log.info("sort data")
        self.data = sorted(
            self.data, key=self.sort_priority_name, reverse=False)
        for channel in self.data:
            channel_data = sorted(
                channel.get("channel_data"), key=self.sort_name)
            channel["channel_data"] = channel_data

    def create_m3u_line(self, meta, source):
        broken = source.get("broken")
        if broken and (broken == "true" or broken is True):
            return ""

        line = "#EXTINF:-1"

        tvg_id = meta.get("tvg-id")
        if tvg_id:
            line += " tvg-id=\"{0}\"".format(tvg_id)

        tvg_name = meta.get("tvg-name")
        if tvg_name:
            line += " tvg-name=\"{0}\"".format(tvg_name)

        tvg_shift = meta.get("tvg-shift")
        if tvg_shift:
            line += " tvg-shift=\"{0}\"".format(tvg_shift)

        group = meta.get("group")
        if group:
            line += " group-title=\"{0}\"".format(";".join(group))

        radio = meta.get("radio")
        if radio == "true":
            line += " radio=\"{0}\"".format(radio)

        tvg_logo = meta.get("tvg-logo")
        if tvg_logo:
            line += " tvg-logo=\"{0}{1}\"".format(
                self.config_data.get("logopath"), tvg_logo)

        line += ",{0}\n".format(source.get("name", "???"))

        url = source.get("url")

        if (source.get("type") == "livecli" or source.get("type") == "streamlink"):
            params = {}
            params["url"] = quote_plus(url)
            streamlink_data = (source.get("streamlink_data") or source.get("livecli_data"))
            if streamlink_data:
                if isinstance(streamlink_data, list):
                    for _data in streamlink_data:
                        if isinstance(_data, tuple):
                            params[quote_plus(_data[0])] = quote_plus(_data[1])
                        elif isinstance(_data, dict):
                            for _y in _data.keys():
                                params[quote_plus(_y)] = quote_plus(_data[_y])
                elif isinstance(streamlink_data, dict):
                    for _y in streamlink_data.keys():
                        params[quote_plus(_y)] = quote_plus(streamlink_data[_y])
                else:
                    log.error('invalid instance for streamlink data')
            line += self.base_proxy + urlencode(params)
        elif source.get("type") == "m3u8":
            params = [url]
            m3u8_data = source.get("m3u8_data")
            if m3u8_data:
                if isinstance(m3u8_data, list):
                    for _data in m3u8_data:
                        if isinstance(_data, tuple):
                            params += ["{0}={1}".format(_data[0], _data[1])]
                        elif isinstance(_data, dict):
                            for _y in _data.keys():
                                params += ["{0}={1}".format(_y, _data[_y])]
                elif isinstance(m3u8_data, dict):
                    for _y in m3u8_data.keys():
                        params += ["{0}={1}".format(_y, m3u8_data[_y])]
                else:
                    log.error('invalid instance for m3u8 data')
            line += "|".join(params)
        line += "\n"
        return line

    def split_data(self):
        log.info("split data")
        iptv_list = []
        iptv_list += ["#EXTM3U\n"]

        for channel in self.data:
            for source_channel in channel.get("channel_data"):
                iptv_list += [self.create_m3u_line(channel, source_channel)]
        return "".join(iptv_list)

    def write_data(self, iptv_list):
        log.info("write data")
        with open(self.config_data.get("filename"), "w") as playlist:
            playlist.write(iptv_list)
        playlist.close()

    def run(self):
        self.read_config()
        self.base_proxy = "http://{0}:{1}/play/?".format(
            self.config_data.get("host"), self.config_data.get("port"))
        self.sort_data()
        iptv_list = self.split_data()
        self.write_data(iptv_list)


if __name__ == "__main__":
    IPTV()
