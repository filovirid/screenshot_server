# Here you can change the default configurations.

config = {
    # HAR logs are collected using 'performance' log in chrome.
    # this type of log only gives you all the requests until the page load is complete.
    # this means you can not collect data from AJAX requests.
    # to collect AJAX requests, you need to install a proxy server
    # in your machine and pass the ip:port to as 'proxy' parameter to the API.
    # if you do not need HAR logs, change the following value
    # by commenting out the '"bmp":1' and uncommenting '"bmp":0' line.
    # The default value is 1 which means browsermob proxy is enabled.
    "HAR":1     # enable HAR log (default)
    #"HAR":0    # disable HAR log
}
