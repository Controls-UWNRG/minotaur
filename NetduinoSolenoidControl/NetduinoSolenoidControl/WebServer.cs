/* HTTP Server running on Netduino to service 
 * commmands from python module. */

using System;
using System.Net.Sockets;
using System.Net;
using System.Threading;
using System.Text;
using Microsoft.SPOT.Hardware;
using SecretLabs.NETMF.Hardware.Netduino;
using Microsoft.SPOT;

namespace NetduinoSolenoidControl
{
    public class WebServer : IDisposable
    {
        private Socket socket = null;
        private const int MaximumValue = 1023;
        private const double AnalogReference = 3.3f;
        private const double SENSOR_RESISTANCE = 0.5;
        
        private OutputPort sol_under = new OutputPort(Pins.GPIO_PIN_D4, true);
        private OutputPort sol_top = new OutputPort(Pins.GPIO_PIN_D0, false);
        private OutputPort sol_bot = new OutputPort(Pins.GPIO_PIN_D1, false);
        private OutputPort sol_left = new OutputPort(Pins.GPIO_PIN_D2, false);
        private OutputPort sol_right = new OutputPort(Pins.GPIO_PIN_D3, false);

        private int SPIN_CONSTANT = 80;
        private int DELAY = 1;
        private int RIGHT_DELAY = 1;

        public WebServer()
        {
            this.sol_under.Write(true);
            this.sol_top.Write(false);
            this.sol_bot.Write(false);
            this.sol_left.Write(false);
            this.sol_right.Write(false);
            
            //Initialize Socket class
            socket = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);
            //Request and bind to an IP from DHCP server
            socket.Bind(new IPEndPoint(IPAddress.Any, 80));
            //Debug print our IP address
            Debug.Print(Microsoft.SPOT.Net.NetworkInformation.NetworkInterface.GetAllNetworkInterfaces()[0].IPAddress);
            //Start listening for web requests
            socket.Listen(10);
            ListenForRequest();
        }

        public string handleCommand(OutputPort sol, string command)
        {
            if (command == "ON")
            {
                sol.Write(true);
                int uselessCounter = 0;
                //for (int i = 0; i < SPIN_CONSTANT; ++i)
                //{
                //    /*if (i == 35)
                //    {
                //        this.sol_under.Write(true);
                //    }
                //    else if (i == 42)
                //    {
                //        this.sol_under.Write(false);
                //    }*/
                //    uselessCounter++;
                    
                //}
                //Thread.Sleep(DELAY);
                //sol.Write(false);
                return "on " + uselessCounter;

            }
            else if (command == "OFF")
            {
                sol.Write(false);
                return "off";
            }
            return "invalid command";
        }

        public void ListenForRequest()
        {
            while (true)
            {
                using (Socket clientSocket = socket.Accept())
                {
                    //Get clients IP
                    IPEndPoint clientIP = clientSocket.RemoteEndPoint as IPEndPoint;
                    EndPoint clientEndPoint = clientSocket.RemoteEndPoint;
                    //int byteCount = cSocket.Available;
                    int bytesReceived = clientSocket.Available;
                    if (bytesReceived > 0)
                    {
                        //Get request
                        byte[] buffer = new byte[bytesReceived];
                        int byteCount = clientSocket.Receive(buffer, bytesReceived, SocketFlags.None);
                        string request = new string(Encoding.UTF8.GetChars(buffer));
                        Debug.Print(request);
                        
                        string response = "";
                        
                        //Blink the onboard
                        string[] words = request.Split(' ');

                        if (words[1] == "1")
                        {
                            response = handleCommand(this.sol_top, words[0]) + " top";
                        }
                        else if (words[1] == "2")
                        {
                            response = handleCommand(this.sol_bot, words[0]) + " bot";
                        }
                        else if (words[1] == "3")
                        {
                            response = handleCommand(this.sol_left, words[0]) + " left";
                        }
                        else if (words[1] == "4")
                        {
                            response = handleCommand(this.sol_right, words[0]) + " right";
                        }
                        else if (words[1] == "5") //brake   
                        {
                            response = handleCommand(this.sol_under, words[0]);
                        }

                        //Compose a response
                        string header = "HTTP/1.0 200 OK\r\nContent-Type: text; charset=utf-8\r\nContent-Length: " + response.Length.ToString() + "\r\nConnection: close\r\n\r\n";
                        clientSocket.Send(Encoding.UTF8.GetBytes(header), header.Length, SocketFlags.None);
                        clientSocket.Send(Encoding.UTF8.GetBytes(response), response.Length, SocketFlags.None);
                    }
                }
            }
        }
        #region IDisposable Members
        ~WebServer()
        {
            Dispose();
        }
         
        public void Dispose()
        {
            if (socket != null)
                socket.Close();
        }
        #endregion
    }
}

