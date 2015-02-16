#!/usr/bin/python

from mmap import mmap
import sys, time, struct, getopt

#REGISTER
GPR_offset = 0x020E0000
GPR_size = 0x020E0fff-GPR_offset
GPIO1_PAD = 0x5F4

#WRITE REGISTER
def writeRegister(arg):
  with open("/dev/mem", "r+b" ) as f:
    mem = mmap(f.fileno(), GPR_size, offset=GPR_offset)

  reg_status = int(arg,16)
  mem[GPIO1_PAD:GPIO1_PAD+4] = struct.pack("<L", reg_status)

#READ REGISTER
def readRegister():
  with open("/dev/mem", "r+b" ) as f:
    mem = mmap(f.fileno(), GPR_size, offset=GPR_offset)

  packed_reg = mem[GPIO1_PAD:GPIO1_PAD+4]
  reg_status = struct.unpack("<L", packed_reg)[0]

  print "READ: "
  print format(reg_status,'#04X')


#ENTRY POINT
def main(argv):
   try:
     opts, args = getopt.getopt(argv,"hrw:")
   except getopt.GetoptError:
     print 'dkio.py -r -w 0xDEADBEEF'
     sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print 'dkio.py -r -w 0xDEADBEEF'
         sys.exit()
      elif opt in ("-r", "--read"):
         readRegister()
      elif opt in ("-w", "--write"):
         writeRegister(arg)

if __name__ == "__main__":
   main(sys.argv[1:])
