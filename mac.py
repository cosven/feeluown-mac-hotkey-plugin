# -*- coding=utf8 -*-

import asyncio
import logging
import os
import socket

logger = logging.getLogger(__name__)

APP = None


def send_cmd(cmd):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('0.0.0.0', 23333))
    sock.recv(1024)
    sock.sendall(bytes(cmd, 'utf-8') + b'\n')
    sock.close()


def keyboard_tap_callback(proxy, type_, event, refcon):
    global APP
    from AppKit import NSKeyUp, NSEvent, NSBundle
    NSBundle.mainBundle().infoDictionary()['NSAppTransportSecurity'] =\
        dict(NSAllowsArbitraryLoads=True)
    if type_ < 0 or type_ > 0x7fffffff:
        logger.error('Unkown mac event')
        run_event_loop()
        logger.error('restart mac key board event loop')
        return event
    try:
        key_event = NSEvent.eventWithCGEvent_(event)
    except:
        logger.info("mac event cast error")
        return event
    if key_event.subtype() == 8:
        key_code = (key_event.data1() & 0xFFFF0000) >> 16
        key_state = (key_event.data1() & 0xFF00) >> 8
        if key_code in (16, 19, 20):
            # 16 for play-pause, 19 for next, 20 for previous
            if key_state == NSKeyUp:
                if key_code is 19:
                    logger.info('mac hotkey: play next')
                    send_cmd('next')
                elif key_code is 20:
                    logger.info('mac hotkey: play last')
                    send_cmd('previous')
                elif key_code is 16:
                    os.system('echo "play_pause" | nc -4u -w0 localhost 8000')
                    send_cmd('toggle')
            return None
    return event


def run_event_loop():
    logger.info("try to load mac hotkey event loop")
    import Quartz
    from AppKit import NSSystemDefined

    # Set up a tap, with type of tap, location, options and event mask
    tap = Quartz.CGEventTapCreate(
        Quartz.kCGSessionEventTap,  # Session level is enough for our needs
        Quartz.kCGHeadInsertEventTap,  # Insert wherever, we do not filter
        Quartz.kCGEventTapOptionDefault,
        # NSSystemDefined for media keys
        Quartz.CGEventMaskBit(NSSystemDefined),
        keyboard_tap_callback,
        None
    )

    run_loop_source = Quartz.CFMachPortCreateRunLoopSource(
        None, tap, 0)
    Quartz.CFRunLoopAddSource(
        Quartz.CFRunLoopGetCurrent(),
        run_loop_source,
        Quartz.kCFRunLoopDefaultMode
    )
    # Enable the tap
    Quartz.CGEventTapEnable(tap, True)
    # and run! This won't return until we exit or are terminated.
    Quartz.CFRunLoopRun()
    logger.error('Mac hotkey event loop exit')
    return []


@asyncio.coroutine
def run(app):
    global APP
    APP = app
    loop = asyncio.get_event_loop()
    future = loop.run_in_executor(None, run_event_loop)
    yield from future
    logger.info('mac hotkey loop end')
