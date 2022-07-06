def recv(self):
		sock = socket.socket(socket.AF_INET,
			socket.SOCK_RAW,
			self.stype)
		sock.bind(('', self.srcp))
		sock.settimeout(5)
		self.events['recv'].wait()
		counter = 0
		while self.events['recv'].isSet():
			try:
				data, sa_ll = sock.recvfrom(65535)
				if self.__CookieCheck(data):
					self.queue.put(Extract(data))
					counter += 1
					if counter==self.count:
						self.events['send'].clear()
						break
			except socket.timeout:
				continue

		sock.close()
		logging.info('[RECV] Received: {} packets'.format(counter))