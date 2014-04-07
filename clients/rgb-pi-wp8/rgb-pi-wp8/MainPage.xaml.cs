using System;
using System.Collections.Generic;
using System.Linq;
using System.Net;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Navigation;
using Microsoft.Phone.Controls;
using Microsoft.Phone.Shell;
using RGB.Resources;
using System.Threading;
using Coding4Fun.Toolkit.Controls;

namespace RGB
{
    public partial class MainPage : PhoneApplicationPage
    {
        private SocketClient client = new SocketClient();
        private Thread worker;
        private ColorPicker copickDimColor;
        private ColorPicker colorPicker;
        private ColorPicker copickPulseStart, copickPulseEnd;

        private readonly Queue<string> commandQ = new Queue<string>();

        public enum RGBCommandType
        {
            ChangeColor = 1,
            RandomFader = 2,
            FadeColor = 3,
            Specials = 4,
            Pulse = 5
        }

        /// <summary>
        /// returns json object as string for the given command.
        /// cc      - 0=color
        /// fade    - 0=time 1=end [2=start]
        /// pulse   - 0=time 1=color1 2=color2
        /// rndfade - 0=minTime 1=maxTime 2=minColor 3=maxColor
        /// 
        /// </summary>
        /// <param name="cmdType"></param>
        /// <param name="p"></param>
        /// <returns></returns>
        public static string GetJSON(RGBCommandType cmdType, params object[] p)
        {
            string json = "{}";
            switch (cmdType)
            {
                case RGBCommandType.ChangeColor:
                    json = "{'commands':[{'type':'cc', 'color':'"+p[0]+"'}]}";
                    break;

                case RGBCommandType.FadeColor:
                    if(p.Length > 2)
                        json = "{'commands':[{'type':'fade', 'time':'" + p[0] + "', 'start':'" + p[2] + "', 'end':'" + p[1] + "'}]}";
                    else
                        json = "{'commands':[{'type':'fade', 'time':'" + p[0] + "', 'end':'" + p[1] + "'}]}";
                    break;

                case RGBCommandType.Pulse:
                    json = @"{
                        'commands':[
                            {
                                'type':'loop',
                                'condition':'{b:1}',
                                'commands':
                                [
                                    {
                                        'type':'fade',
                                        'time':'"+p[0]+@"',
                                        'end':'" + p[1] + @"'
                                    },

                                    {
                                        'type':'fade',
                                        'time':'" + p[0] + @"',
                                        'end':'" + p[2] + @"'
                                    }
                                ]
                            }
                        ]
                    }";
                    break;

                case RGBCommandType.RandomFader:
                    string mCmC = "{r:" + p[2] + "-" + p[3] + "," + p[2] + "-" + p[3] + "," + p[2] + "-" + p[3] + "}";

                    json = @"{
                        'commands':[
                            {
                                'type':'loop',
                                'condition':'{b:1}',
                                'commands':
                                [
                                    {
                                        'type':'fade',
                                        'time':'{r:"+p[0]+@","+p[1]+@"}',
                                        'end':'" + mCmC + @"'
                                    },

                                    {
                                        'type':'fade',
                                        'time':'{r:" + p[0] + @"," + p[1] + @"}',
                                        'end':'" + mCmC + @"'
                                    }
                                ]
                            }
                        ]
                    }";
                    break;

                case RGBCommandType.Specials:

                    break;

                
            }

           //TODO: workaround to be able to set '' instead of "" for strings and keys
            json = json.Replace("'", "\"");

            return json;
        }

       
        // Constructor
        public MainPage()
        {
            InitializeComponent();

            // Set the data context of the listbox control to the sample data
            DataContext = App.ViewModel;

            // Sample code to localize the ApplicationBar
            BuildLocalizedApplicationBar();

            colorPicker = new ColorPicker();
            colorPicker.ColorChanged += colorPicker_ColorChanged;
            gridChooseColor.Children.Add(colorPicker);

            copickDimColor = new ColorPicker();
            gridDimColor.Children.Add(copickDimColor);

            copickPulseStart = new ColorPicker();
            copickPulseEnd = new ColorPicker();
            gridPulseStartColor.Children.Add(copickPulseStart);
            gridPulseEndColor.Children.Add(copickPulseEnd);


            worker = new Thread(rgbWorking);
            worker.IsBackground = true;
            worker.Start();

        }

        void colorPicker_ColorChanged(object sender, System.Windows.Media.Color color)
        {
            lock (commandQ)
            {
                if (commandQ.Count > 0) commandQ.Clear();
                commandQ.Enqueue(GetJSON(RGBCommandType.ChangeColor, new LEDColor(color)));
                Monitor.PulseAll(commandQ);
            }
        }


        private void rgbWorking()
        {
            while (true)
            {
                try
                {
                    string cmd;
                    lock (commandQ)
                    {

                        while (commandQ.Count == 0)
                        {
                            Monitor.Wait(commandQ, 1000);
                        }


                        cmd = commandQ.Dequeue();
                    }


                    client.Connect("192.168.1.150", 4321);
                    client.Send(cmd);
                    string answer = client.Receive();
                    client.Close();
                    
                }
                catch { }
            }
        }


        // Load data for the ViewModel Items
        protected override void OnNavigatedTo(NavigationEventArgs e)
        {
            if (!App.ViewModel.IsDataLoaded)
            {
                App.ViewModel.LoadData();
            }
        }



        // Sample code for building a localized ApplicationBar
        private void BuildLocalizedApplicationBar()
        {
            // Set the page's ApplicationBar to a new instance of ApplicationBar.
            ApplicationBar = new ApplicationBar();

            // Create a new button and set the text value to the localized string from AppResources.
            ApplicationBarIconButton abbOn = new ApplicationBarIconButton(new Uri("/Assets/Icons/on.png", UriKind.Relative));
            abbOn.Text = "On";
            abbOn.Click += delegate(object s, EventArgs ea)
            {
                lock (commandQ)
                {
                    commandQ.Enqueue(GetJSON(RGBCommandType.FadeColor, 2, new LEDColor(1f, 1f, 1f)));
                    //commandQ.Enqueue(new RGBCommand(RGBCommandType.FadeColor, "2 "+new LEDColor(1f, 1f, 1f)));
                    Monitor.PulseAll(commandQ);
                }
            };
            ApplicationBar.Buttons.Add(abbOn);

            ApplicationBarIconButton abbOff = new ApplicationBarIconButton(new Uri("/Assets/Icons/off.png", UriKind.Relative));
            abbOff.Text = "Off";
            abbOff.Click += delegate(object s, EventArgs ea)
            {
                lock (commandQ)
                {
                    commandQ.Enqueue(GetJSON(RGBCommandType.FadeColor, 2, new LEDColor()));
                    //commandQ.Enqueue(new RGBCommand(RGBCommandType.FadeColor, "2 "+new LEDColor()));
                    Monitor.PulseAll(commandQ);
                }
            };
            ApplicationBar.Buttons.Add(abbOff);

            // Create a new menu item with the localized string from AppResources.
            ApplicationBarMenuItem appBarMISettings = new ApplicationBarMenuItem("settings");
            appBarMISettings.Click += delegate(object s, EventArgs ea)
            {
                NavigationService.Navigate(new Uri("/Settings.xaml", UriKind.Relative));
            };
            ApplicationBar.MenuItems.Add(appBarMISettings);
        }

       

        private void btnDim_Click(object sender, RoutedEventArgs e)
        {
            lock (commandQ)
            {
                commandQ.Enqueue(GetJSON(RGBCommandType.FadeColor, (slideDimTime.Value >= 60 ? (int)slideDimTime.Value - (((int)slideDimTime.Value) % 60) : (int)slideDimTime.Value), new LEDColor(), new LEDColor(copickDimColor.Color)));
                //commandQ.Enqueue(new RGBCommand(RGBCommandType.FadeColor, (slideDimTime.Value >= 60 ? (int)slideDimTime.Value - (((int)slideDimTime.Value) % 60) : (int)slideDimTime.Value) + " " + new LEDColor() + " " + new LEDColor(copickDimColor.Color)));
                Monitor.PulseAll(commandQ);
            }
        }

        private void btnSpecialsJamaica_Click(object sender, RoutedEventArgs e)
        {
            lock (commandQ)
            {
                //commandQ.Enqueue(new RGBCommand(RGBCommandType.Specials, "jamaica 2"));
                Monitor.PulseAll(commandQ);
            }
        }

        private void slideDimTime_ValueChanged(object sender, RoutedPropertyChangedEventArgs<double> e)
        {
            if (slideDimTime == null)
                return;

            int s = (int)slideDimTime.Value;
            

            if(s <= 60)
                btnDim.Content = "Dim over "+s+" seconds";
            else
                btnDim.Content = "Dim over " + (s/60) + " minutes";
        }


        private void sliderPulseTime_ValueChanged(object sender, RoutedPropertyChangedEventArgs<double> e)
        {
            if (btnPulseStart != null) btnPulseStart.Content = "start pulse (interval = " + ((int)sliderPulseTime.Value) + " second" + (sliderPulseTime.Value >= 2 ? "s" : "") + ")";
        }

        private void btnPulseStart_Click(object sender, RoutedEventArgs e)
        {
            lock (commandQ)
            {
                commandQ.Enqueue(GetJSON(RGBCommandType.Pulse, (int)sliderPulseTime.Value, new LEDColor(copickPulseStart.Color), new LEDColor(copickPulseEnd.Color)));
                //commandQ.Enqueue(new RGBCommand(RGBCommandType.Pulse, ((int)sliderPulseTime.Value)+" "+new LEDColor(copickPulseStart.Color)+" "+new LEDColor(copickPulseEnd.Color)));
                Monitor.PulseAll(commandQ);
            }
        }

        

        private void piDim_Loaded(object sender, RoutedEventArgs e)
        {
            copickDimColor.Color = colorPicker.Color;
        }

        private void btnRF_Click(object sender, RoutedEventArgs e)
        {
            lock (commandQ)
            {
                commandQ.Enqueue(GetJSON(RGBCommandType.RandomFader, ((int)slideMinTime.Value), ((int)slideMaxTime.Value), (slideMinBrightness.Value / 100f).ToString("F3").Replace(",", "."), (slideMaxBrightness.Value / 100f).ToString("F3").Replace(",", ".")));
                //commandQ.Enqueue(new RGBCommand(RGBCommandType.RandomFader, ((int)slideMinTime.Value) + " " + ((int)slideMaxTime.Value) + " " + (slideMinBrightness.Value / 100f).ToString("F3").Replace(",", ".") + " " + (slideMaxBrightness.Value / 100f).ToString("F3").Replace(",", ".")));
                Monitor.PulseAll(commandQ);
            }
        }


    }

}