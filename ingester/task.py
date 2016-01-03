#
# Abstract job class that all other ingester tasks inherit from
#


class Job(object):

	def __init__(self):
		raise NotImplementedError()

	def run(self):
		raise NotImplementedError()

