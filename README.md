# flashcookies - A shell tool for reading Flash cookies

`flashcookies` is a shell tool to manipualte Flash cookies (.sol Flash SharedObject files).

## Examples

List all objects stored by Google:

    $ flashcookies --list '*google.com'
    2EUWQE47/mail.google.com/wakeup.sol
    2EUWQE47/video.google.com/videostats.sol
    N8Q2CNW7/video.google.com/videostats.sol

Dump all `videostats` objects held by `video.google.com` as YAML:

    $ flashcookies -f yaml video.google.com videostats
    perf:
    - bytes: 1162098
      time: 1.8959999999999999
    - bytes: 1072968
      time: 5.1620000000000008
    - bytes: 1234256
      time: 7.7540000000000004
    - bytes: 1098268
      time: 1.694
    ---
    perf:
    - bytes: 1104824
      time: 1.617
    - bytes: 1074416
      time: 1.5939999999999999


## Feedback

Open a ticket on [github](http://github.com/dsc/flashcookies), or send me an email at [dsc@less.ly](mailto:dsc@less.ly).
