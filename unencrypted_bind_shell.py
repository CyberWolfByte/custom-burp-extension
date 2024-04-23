from burp import IBurpExtender, ITab
from javax import swing
from java.awt import BorderLayout
import sys, time, socket, threading, sys
from exceptions_fix import FixBurpExceptions # Correct import path

# Burp extension to interact with a bind shell
class BurpExtender(IBurpExtender, ITab):
	# Initialize and set up the UI components for the extension
	def registerExtenderCallbacks(self, callbacks):
		# Variables to control the extension state
		self.clicked = False
		self.response_data = None
		self.kill_threads = False
		sys.stdout = callbacks.getStdout() # Redirect stdout to Burp's console

		self.callbacks = callbacks
		self.callbacks.setExtensionName("Bind Shell")
		self.tab = swing.JPanel(BorderLayout())

		# Setting up the UI components
		text_panel = swing.JPanel()
		box_vertical = swing.Box.createVerticalBox()

		box_horizontal = swing.Box.createHorizontalBox()
		self.ip_address = swing.JTextArea('', 2, 100)
		self.ip_address.setLineWrap(True)
		self.ip_address.border = swing.BorderFactory.createTitledBorder("IP Address:")
		box_horizontal.add(self.ip_address)
		box_vertical.add(box_horizontal)

		box_horizontal = swing.Box.createHorizontalBox()
		self.user_command = swing.JTextArea('', 2, 100)
		self.user_command.setLineWrap(True)
		self.user_command.border = swing.BorderFactory.createTitledBorder("Command:")
		box_horizontal.add(self.user_command)
		box_vertical.add(box_horizontal)

		box_horizontal = swing.Box.createHorizontalBox()
		button_panel = swing.JPanel()

		self.connect_button = swing.JButton('[ --- Connect --- ]', actionPerformed=self.connect)
		self.send_button = swing.JButton('[ --- Send Command --- ]', actionPerformed=self.execute_command)
		self.disconnect_button = swing.JButton('[ --- Disconnect --- ]', actionPerformed=self.disconnect)

		self.disconnect_button.enabled = False
		self.send_button.enabled = False

		button_panel.add(self.connect_button)
		button_panel.add(self.send_button)
		button_panel.add(self.disconnect_button)

		box_horizontal.add(button_panel)
		box_vertical.add(box_horizontal)

		box_horizontal = swing.Box.createHorizontalBox()
		self.output = swing.JTextArea('', 25, 100)
		self.output.setLineWrap(True)
		self.output.setEditable(True)

		scroll = swing.JScrollPane(self.output)

		box_horizontal.add(scroll)
		box_vertical.add(box_horizontal)

		text_panel.add(box_vertical)

		self.tab.add(text_panel)

		callbacks.addSuiteTab(self)
		return

	def getTabCaption(self):
		return "Bind Shell"

	def getUiComponent(self):
		return self.tab

	# Executing command on the remote shell
	def execute_command(self, event):
	    command_text = self.user_command.text.strip() + "\n"
	    try:
	        self.client_socket.send(command_text.encode('utf-8'))
	        self.user_command.text = ""
	    except Exception as e:
	        self.output.text += "\nFailed to send command: " + str(e)

	# Thread functions for sending commands and receiving output
	def send_commands(self):
		# Thread function for handling command sending
		while True:
			if self.kill_threads:
				sys.exit()
			if self.clicked:
				self.clicked = False
				self.client_socket.send(self.user_command.text)

	def receive_output(self):
		# Thread function for handling output receiving
	    while True:
	        if self.kill_threads:
	            break
	        try:
	            output = self.client_socket.recv(4096).decode('utf-8')
	            # Directly append received output to the UI, without replacing specific strings
	            # Ensure UI updates happen in the Swing event dispatch thread for thread safety
	            swing.SwingUtilities.invokeLater(lambda: self.output.append(output + "\n"))
	        except socket.error as e:
	            print("Socket error: ", e)
	            break

	def connect(self, event):
		# Handles establishing connection to the bind shell
	    try:
	        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	        ip_address_text = self.ip_address.text.strip()
	        self.client_socket.connect((ip_address_text, 1234))  # Ensure IP address text is cleaned
	        self.kill_threads = False

	        # Start threads
	        threading.Thread(target=self.send_commands).start()
	        threading.Thread(target=self.receive_output).start()

	        # Update UI components
	        self.connect_button.enabled = False
	        self.disconnect_button.enabled = True
	        self.send_button.enabled = True
	        self.ip_address.setEditable(False)

	        self.output.text = "Successfully connected to the remote bind shell.\n"
	    except Exception as e:
	        self.output.text = "A connection error occurred: {}. Please try again.".format(e)

	def disconnect(self, event):
		# Handles disconnecting from the bind shell
	    try:
	        self.client_socket.send("exit".encode('utf-8'))
	        self.client_socket.close()
	        self.kill_threads = True

	        # Reset UI components
	        self.connect_button.enabled = True
	        self.disconnect_button.enabled = False
	        self.send_button.enabled = False
	        self.ip_address.enabled = True
	        self.output.text = "Session terminated. Goodbye!"
	    except Exception as e:
	        self.output.text = "Error during disconnection: {}".format(e)

FixBurpExceptions()