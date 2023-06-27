#!/usr/bin/env python3
import psutil
import logging

logger = logging.getLogger(__name__)


def get():
    interfaces = psutil.net_io_counters(pernic=True, nowrap=True)
    net_interfaces = {}
    network_tmp = {}
    tmp = {}
    for iname in interfaces:
        if interfaces[iname]:
            interface = f'network.net_{iname}'
            stats = interfaces[iname]
            # ^ bytes_sent=0, bytes_recv=0, packets_sent=0, packets_recv=0, errin=0, errout=0, dropin=0, dropout=0
            tmp = {
                interface: {}
            }

            try:
                tmp[interface]['bytes_sent'] = stats.bytes_sent
            except Exception as e:
                tmp[interface]['bytes_sent'] = None
                logger.warning(f'Error occurred while accessing stats.bytes_sent: {e}')

            try:
                tmp[interface]['bytes_recv'] = stats.bytes_recv
            except Exception as e:
                tmp[interface]['bytes_recv'] = None
                logger.warning(f'Error occurred while accessing stats.bytes_recv: {e}')

            try:
                tmp[interface]['packets_sent'] = stats.packets_sent
            except Exception as e:
                tmp[interface]['packets_sent'] = None
                logger.warning(f'Error occurred while accessing stats.packets_sent: {e}')

            try:
                tmp[interface]['packets_recv'] = stats.packets_recv
            except Exception as e:
                tmp[interface]['packets_recv'] = None
                logger.warning(f'Error occurred while accessing stats.packets_recv: {e}')

            try:
                tmp[interface]['errin'] = stats.errin
            except Exception as e:
                tmp[interface]['errin'] = None
                logger.warning(f'Error occurred while accessing stats.errin: {e}')

            try:
                tmp[interface]['errout'] = stats.errout
            except Exception as e:
                tmp[interface]['errout'] = None
                logger.warning(f'Error occurred while accessing stats.errout: {e}')

            try:
                tmp[interface]['dropin'] = stats.dropin
            except Exception as e:
                tmp[interface]['dropin'] = None
                logger.warning(f'Error occurred while accessing stats.dropin: {e}')

            try:
                tmp[interface]['dropout'] = stats.dropout
            except Exception as e:
                tmp[interface]['dropout'] = None
                logger.warning(f'Error occurred while accessing stats.dropout: {e}')

        network_tmp.update(tmp)
    net_interfaces = {'net_interfaces': network_tmp}
    return net_interfaces


def metrics():
    return get()
