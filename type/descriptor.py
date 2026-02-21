from enum import Enum

# 2^16 max config connections per boot is enough i guess??? Maybe, in future, I will un-hardcode it.
# Or I'll just force config reset after limit exceedes.
higherbits = 2**16 | 2**17
class Descriptor(Enum):
	NULL = -1
	DENIED = 0
	READONLY = 2**16
	OWNER = 2**17


	@staticmethod
	def GetType(descriptor):
		typeval = descriptor & higherbits
		for d in Descriptor:
			if d.value == typeval:
				return d
		return Descriptor.NULL

	@staticmethod
	def GetID(descriptor):
		return descriptor & ~higherbits
