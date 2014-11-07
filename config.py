'''
Global configuration file
'''
redis = {
  'host': '10.0.0.13',
  'port': 6379,
}

mongo = {
  'host': '10.0.0.13',
  'port': 27017,
}

pollenc_tcp = {
  'interface': '10.0.0.12', 
  'port': 5140,
}

riemann = {
      'host': '10.0.0.11', 
}

redisQueues = {
  'arm-none-eabi-gcc': 'POLLEN_CLC_ARM_NONE_EABI_GCC_1_0',
  'avr-gcc': 'POLLEN_CLC_AVR_GCC_1_0',
  'efm32-gcc': 'POLLEN_CLC_ARM_NONE_EABI_GCC_1_0',
  'localhost-gcc': 'POLLEN_CLC_LOCALHOST_1_0'
}

clcConstants = {
  'MAX_MSG_SIZE' : 1000000,
}

