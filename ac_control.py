#!/usr/bin/python

# Author: Danny De Gaspari

import lib_serial
import sys, getopt


unit = [0,1]
poweroff = False
fan = 1
temp = 20
mode = 4
opts, args = getopt.getopt(sys.argv[1:],"hu:of:t:m:")
for opt, arg in opts:
  if opt == '-h':
    print sys.argv[0], '-h -u -o -f -t -m'
    print 'options:'
    print '     -h                : help'
    print '     -u <unit nbr>     : AC unit number, all units when omitted'
    print '     -o                : switch AC off'
    print '     -f <fan speed>    : auto, low, med, high'
    print '     -t <temperature>  : temperature in celsius'
    print '     -m <mode>         : auto, cool, dry, fan, heat'
    print '  example 1: ', sys.argv[0], '-u 0 -t 23 -f auto'
    print '  example 2: ', sys.argv[0], '-u 0 -o'
    sys.exit()
  elif opt == '-u':
    unit = [int(arg)]
  elif opt == '-o':
    poweroff = True
  elif opt == '-f':
    if arg == 'auto':
      fan = 1
    elif arg == 'low':
      fan = 2
    elif arg == 'med':
      fan = 4
    elif arg == 'high':
      fan = 6
  elif opt == '-t':
    temp = int(arg)
  elif opt == '-m':
    if arg == 'auto':
      mode = 0
    elif arg == 'cool':
      mode = 1
    elif arg == 'dry':
      mode = 2
    elif arg == 'fan':
      mode = 3
    elif arg == 'heat':
      mode = 4
  #elif opt == '-c':
  #  cmd.append( int(arg,16) )

ser = lib_serial.ser_open()
print 'Capturing on:', ser.name

for i in unit:
  msg = []
  msg.append(0x85 )
  msg.append(0x20 + i )
  msg.append(0xa0 )
  msg.append(0x1a )
  msg.append(0x18 )
  msg.append((fan << 5) + temp)
  msg.append(mode)
  if poweroff:
    msg.append(0xc4 )
  else:
    msg.append(0xf4 )
  msg.append(0x0  )
  msg.append(0x0  )
  msg.append(0x0  )

  sermsg = lib_serial.compose_msg(msg)
  serline = lib_serial.ser_send_msg(ser, sermsg)
  lib_serial.print_serline(serline)

print('The end.')
lib_serial.ser_close(ser)
