# Rocky9 Cluster upgrade

COSMA was upgraded to Rocky Linux 9 in July 2024 (currently Rocky Linux 9.8).

For the original upgrade announcement, see the [Rocky 9 upgrade emails](rocky9email.md).

## Fixes

### gnome-terminal

If gnome-terminal is refusing to start, please try `dbus-launch gnome-terminal` or alternatively, `xfce4-terminal`.

### x2go

Disable the compositor to get rid of shadows when you move screens around. Find this at:
```
Applications > Settings > Window Manager Tweaks > Compositor
```

The screen lock can also be disabled in:
```
Applications > Settings > Xfce Screensaver > Lock Screen
```

Further information about [x2go is here](x2go.md).
