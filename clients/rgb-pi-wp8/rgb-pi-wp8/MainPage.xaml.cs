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
using System.IO.IsolatedStorage;

namespace RGB
{
    public partial class MainPage : PhoneApplicationPage
    {
        private SocketClient client = new SocketClient();
        private Thread worker;
        private ColorPicker copickDimColor;
        private ColorPicker colorPicker;
        private ColorPicker copickPulseStart, copickPulseEnd;

        private readonly Queue<RGBCommand> commandQ = new Queue<RGBCommand>();

        private IsolatedStorageSettings settings = IsolatedStorageSettings.ApplicationSettings;


        public string IP { get; set; }
        public int Port { get; set; }

        private enum RGBCommandType
        {
            ChangeColor = 1,
            RandomFader = 2,
            FadeColor = 3,
            Specials = 4,
            Pulse = 5
        }

        private struct RGBCommand
        {
            public LEDColor Color;
            public RGBCommandType Type;
            public string Command;

            public RGBCommand(RGBCommandType type, LEDColor color)
            {
                Command = string.Empty;
                Type = type;
                Color = color;
            }

            public RGBCommand(RGBCommandType type, float r, float g, float b)
            {
                Command = string.Empty;
                Type = type;
                Color = new LEDColor(r, g, b);
            }

            public RGBCommand(RGBCommandType type, string command)
            {
                this.Command = command;
                Type = type;
                Color = new LEDColor();
            }
        }

        // Constructor
        public MainPage()
        {
            InitializeComponent();

            if (IsolatedStorageSettings.ApplicationSettings.Contains("ip"))
            {
                IP = (string)IsolatedStorageSettings.ApplicationSettings["ip"];
            }
            else
            {
                IsolatedStorageSettings.ApplicationSettings.Add("ip", IP = "192.168.0.10");
            }

            if (IsolatedStorageSettings.ApplicationSettings.Contains("port"))
            {
                Port = int.Parse(IsolatedStorageSettings.ApplicationSettings["port"].ToString());
            }
            else
            {
                IsolatedStorageSettings.ApplicationSettings.Add("port", Port = 4321);
            }


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

        private void LoadSettings()
        {
            settings = IsolatedStorageSettings.ApplicationSettings;
            if (settings.Contains("ip"))
            {
                IP = (string)settings["ip"];
            }
            else
            {
                settings.Add("ip", IP = "192.168.0.10");
            }

            if (settings.Contains("port"))
            {
                Port = int.Parse(settings["port"].ToString());
            }
            else
            {
                settings.Add("port", Port = 4321);
            }
        }

        protected override void OnNavigatedFrom(NavigationEventArgs e)
        {
            base.OnNavigatedFrom(e);
            LoadSettings();
        }

        protected override void OnOrientationChanged(OrientationChangedEventArgs e)
        {
            base.OnOrientationChanged(e);
            LoadSettings();
        }

        void colorPicker_ColorChanged(object sender, System.Windows.Media.Color color)
        {
            lock (commandQ)
            {
                if (commandQ.Count > 0) commandQ.Clear();
                commandQ.Enqueue(new RGBCommand(RGBCommandType.ChangeColor, color.R / 255.0f, color.G / 255.0f, color.B / 255.0f));
                Monitor.PulseAll(commandQ);
            }
        }


        private void rgbWorking()
        {
            while (true)
            {
                try
                {
                    RGBCommand c;
                    lock (commandQ)
                    {

                        while (commandQ.Count == 0)
                        {
                            Monitor.Wait(commandQ, 1000);
                        }


                        c = commandQ.Dequeue();
                    }


                    client.Connect(IP, Port);
                    switch (c.Type)
                    {
                        case RGBCommandType.ChangeColor:
                            client.Send("cc " + c.Color);
                            break;
                        case RGBCommandType.RandomFader:
                            client.Send("rf " + c.Command);
                            break;
                        case RGBCommandType.FadeColor:
                            client.Send("fade " + c.Command);
                            break;
                        case RGBCommandType.Specials:
                            client.Send("special " + c.Command);
                            break;
                        case RGBCommandType.Pulse:
                            client.Send("pulse " + c.Command);
                            break;
                    }
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
                    commandQ.Enqueue(new RGBCommand(RGBCommandType.FadeColor, "2 "+new LEDColor(1f, 1f, 1f)));
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
                    commandQ.Enqueue(new RGBCommand(RGBCommandType.FadeColor, "2 "+new LEDColor()));
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
                commandQ.Enqueue(new RGBCommand(RGBCommandType.FadeColor, (slideDimTime.Value >= 60 ? (int)slideDimTime.Value - (((int)slideDimTime.Value) % 60) : (int)slideDimTime.Value) + " " + new LEDColor() + " " + new LEDColor(copickDimColor.Color)));
                Monitor.PulseAll(commandQ);
            }
        }

        private void btnSpecialsJamaica_Click(object sender, RoutedEventArgs e)
        {
            lock (commandQ)
            {
                commandQ.Enqueue(new RGBCommand(RGBCommandType.Specials, "jamaica 2"));
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
                commandQ.Enqueue(new RGBCommand(RGBCommandType.Pulse, ((int)sliderPulseTime.Value)+" "+new LEDColor(copickPulseStart.Color)+" "+new LEDColor(copickPulseEnd.Color)));
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
                commandQ.Enqueue(new RGBCommand(RGBCommandType.RandomFader, ((int)slideMinTime.Value) + " " + ((int)slideMaxTime.Value) + " " + (slideMinBrightness.Value / 100f).ToString("F3").Replace(",", ".") + " " + (slideMaxBrightness.Value / 100f).ToString("F3").Replace(",", ".")));
                Monitor.PulseAll(commandQ);
            }
        }


    }

}