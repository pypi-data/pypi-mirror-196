# sopel-slap

Plugin for Sopel that lets users slap each other in fun ways

## Installation

```sh
pip install sopel-slap
```

_Substitute the appropriate `pip` command based on your environment (e.g.
`pip3` or `pip3.10` on systems with multiple Python versions available)._

_If your Sopel configuration requires it, run `sopel-plugins enable slap`,
passing the appropriate config name to `-c` if you have multiple bots._

## Commands

* **.slap** — Make the bot slap you
* **.slap nickname [reason]** — Slap someone else, with an optional reason

_If your bot has a non-default `prefix`, substitute it for `.` above._

## Credits

This is based on the original `slap.py` from
[sopel-extras](https://github.com/sopel-irc/sopel-extras) by Michael Yanovich,
dating back to the late '00s/early '10s. It's been rewritten more or less from
scratch to do things in the modern Sopel way. The only meaningful behavior
change was dropping substitution of the caller's nick for `me` and `myself`,
as it's quite possible for a real person to use either of those as a nick and
_no one_\* should be safe from slaps!

\* — No one except the bot and its admins, that is.
