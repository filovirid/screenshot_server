# Here you can change the default configurations.

config = {
    # browsermob-proxy is an open source project at:
    # https://github.com/lightbody/browsermob-proxy
    # It has not been update since 3 years ago and it's deprecated.
    # It is used to collect HAR log but it's not that stable.
    # if you do not need HAR logs, change the following value
    # by commenting out the '"bmp":1' and uncommenting '"bmp":0' line.
    # The default value is 1 which means browsermob proxy is enabled.
    "bmp":1     # enable browsermob-proxy (default)
    #"bmp":0    # disable browsermob-proxy 
}
