# Burp Extension (Windows)

This Burp Suite extension, named "Bind Shell," enables users to interact with a remote bind shell using `unencrypted_bind_shell.py` directly within the Burp Suite environment. It incorporates a user-friendly interface for specifying the target IP address and sending commands, viewing the command output in real-time. This extension transforms Burp Suite from a web application security tool into a versatile platform that can also facilitate remote server management through a bind shell, showcasing the extensibility of Burp Suite through custom extensions.

## Disclaimer

The tools and scripts provided in this repository are made available for educational purposes only and are intended to be used for testing and protecting systems with the consent of the owners. The author does not take any responsibility for the misuse of these tools. It is the end user's responsibility to obey all applicable local, state, national, and international laws. The developers assume no liability and are not responsible for any misuse or damage caused by this program. Under no circumstances should this tool be used for malicious purposes. The author of this tool advocates for the responsible and ethical use of security tools. Please use this tool responsibly and ethically, ensuring that you have proper authorization before engaging any system with the techniques demonstrated by this project.

## Prerequisites

- **Operating System**: Tested with Windows 10 x64, version 22H2.
- **Python Version**: Python 3.x
- **Burp Suite**: Tested with Burp Suite Community Edition v2023.12.1.5 https://portswigger.net/burp/communitydownload
- **Jython**: Provides implementations of Python in Java for running JVM and accessing classes written in Java. Tested with Jython is 2.7.3. https://www.jython.org/download
- **Burp Exceptions Script**: Increase readability of exceptions raised by Burp extensions written in Python. https://github.com/securityMB/burp-exceptions/

## Installation

### Burp Suite Community Edition with Jython

1. **Download Burp Suite Community Edition:**
    - **Visit the PortSwigger Website:** Open your web browser and navigate to the official PortSwigger website at `https://portswigger.net/burp/communitydownload`.
    - **Choose Your Edition:** Click on the "Download" button for the Community Edition. You might need to register or log in if prompted.
2. **Install Burp Suite Community Edition:**
    - **Run the Installer:** Once the download is complete, locate the installer file (typically named `burpsuite_community_<version>.exe`) and double-click it to start the installation process.
    - **Follow Installation Prompts:** Proceed through the installation wizard. Accept the license agreement, choose your preferred installation directory, and follow the on-screen instructions to complete the installation.
3. **Configure Java Runtime Environment (Optional):**
    - Burp Suite requires Java to run. If you don't have Java installed or if Burp Suite cannot find your Java installation, you'll need to install or configure Java:
    - **Download Java:** Download the latest version of Java Runtime Environment (JRE) from the official Oracle website or adopt a JRE like AdoptOpenJDK.
    - **Install Java:** Run the downloaded Java installer and follow the instructions to install Java on your system.
    - **Set JAVA_HOME Environment Variable (Optional):** Set the `JAVA_HOME` environment variable to the path where Java is installed. This step helps some applications, including Burp Suite, to locate the Java installation.
4. **Launch Burp Suite Community Edition:**
    - **Start Burp Suite:** After installation, launch Burp Suite Community Edition by clicking on the Burp Suite icon created on your desktop or searching for Burp Suite in the Start menu.
5. **Setting Up Jython in Burp Suite:**
    - Integrating Jython allows you to write or use Burp Suite extensions in Python, expanding the capabilities of Burp Suite with custom functionality.
    - **Download Jython:** Go to the Jython official website and download the latest standalone Jython JAR file.
    - **Configure Jython in Burp Suite:**
        1. Launch Burp Suite.
        2. Navigate to the “Extensions” tab and then select the “Extensions settings” sub-tab.
        3. In the "Python Environment" section, click on the "Select file..." button next to "Location of Jython standalone JAR file".
        4. Browse to the location where you downloaded the Jython standalone JAR file, select it, and click "Open".
6. **Setting Up `exceptions_fix.py`:**
    - **Download the `exceptions_fix.py` Script:**
        - Visit the [Burp Exceptions GitHub page](https://github.com/securityMB/burp-exceptions) to find the `exceptions_fix.py` script.
        - Download the `exceptions_fix.py` file by either directly saving it from the GitHub webpage or by cloning the repository to your local machine using Git.
    - **Save the Script for Development Use:**
        - Save the `exceptions_fix.py` file in the directory where you plan to develop your custom Burp extension. This script is intended to be used as part of your development environment rather than being loaded directly into Burp Suite as an extension.
        - Add the directory containing `exception_fix.py` to the "Folder for loading modules (optional)" field under the “Extensions” tab > “Extensions settings”.
    - **Integrate `exceptions_fix.py` with Your Extension:**
        - To use it, make sure to import the necessary functions or classes from `exceptions_fix.py` at the beginning of your extension script.
    - **Load the Custom Extension:**
        - Load your Python script in Burp Suite by navigating to “Extensions” > “Installed” then click on “Add” in the “Burp extensions” section.
        - In the “Load Burp extension” window, under the “Extension details” section, select “Python” from the drop-down menu for “Extension type” then click “Select file” to load your Python script for “Extension file.(py)”. Click “Next” to load your extension and ensure no errors are present.
            ![BurpSuite Custom Extension](/images/load_custom_extension.png)
## Usage

1. **Running the Bind Shell Script**:
    - Start the server script in one terminal:
        
        ```bash
        python unencrypted_bind_shell.py -l
        ```
        
    - Connect from the client using the Bind Shell custom tab in the Burp Suite UI. Enter the IP address and port number then click `Connnect` button to establish a connection with the server.
        
        ```bash
        IP Address: 127.0.0.1
        Command: 1234
        ```
        
2. **Interactive Usage**:
    - Use the `Send Command` button to send commands from the client to the server.
    - The server script records incoming commands. Observe command execution results returned to the client for verification in the Bind Shell tab console.
    - Click `Disconnect` button to terminate session.

## How It Works

- **Extension Setup**: Implements `IBurpExtender` and `ITab` for integration into Burp Suite, setting up a custom tab in the UI.
- **UI Components**: Utilizes Swing components to create a simple yet effective user interface including text areas for IP and command input, buttons for connect, send, and disconnect actions, and a large output area for displaying responses.
- **Functionality**: Connects to the specified IP address on port `1234` to send shell commands and receive responses. It supports real-time interaction with the bind shell server for executing remote commands.
- **Threading**: Uses threads to handle command sending and output receiving without blocking the UI, ensuring a smooth user experience.
- **Safety and Cleanup**: Provides a disconnect function to cleanly close the socket connection and terminate threads when finished.

## Output Example

![BurpSuite Bind Shell Connection](/images/bind_shell_connection.png)

![BurpSuite Bind Shell Results](/images/bind_shell_results.png)

![BurpSuite Close Connection](/images/terminate_connection.png)

![Server Command Execution](/images/server_commands.png)

## Contributing

If you have an idea for an improvement or if you're interested in collaborating, you are welcome to contribute. Please feel free to open an issue or submit a pull request.

## License

This project is licensed under the GNU General Public (GPL) License - see the [LICENSE](LICENSE) file for details.
