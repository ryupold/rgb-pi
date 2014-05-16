using System;
using System.Collections.Generic;
using System.Linq;
using System.Runtime.InteropServices.WindowsRuntime;
using Windows.UI;
using Windows.UI.Xaml;
using Windows.UI.Xaml.Controls;
using Windows.UI.Xaml.Data;
using Windows.UI.Xaml.Documents;
using Windows.UI.Xaml.Input;
using Windows.UI.Xaml.Media;

// The Templated Control item template is documented at http://go.microsoft.com/fwlink/?LinkId=234235

namespace Windows8
{
    public class Color
    {
        private float r, g, b;

        public float R { get; private set; }
        public float G { get; private set; }
        public float B { get; private set; }


        public Color(float r, float g, float b)
        {
            R = r;
            G = g;
            B = b;
        }

        public Color(byte r, byte g, byte b)
        {
            R = r / 255f;
            G = g / 255f;
            B = b / 255f;
        }

        /// <summary>
        /// 
        /// </summary>
        /// <param name="h">0 - 360</param>
        /// <param name="s">0 - 1</param>
        /// <param name="v">0 - 1</param>
        /// <returns></returns>
        public static Color FromHSV(float h, float s, float v)
        {
            float M = v;
            float m = M * (1 - s);
            float z = (M-m)*(1 - Math.Abs((h/60f) % 2 - 1));

            float r = 0;
            float g = 0;
            float b = 0;

            if(h < 60)
            {
                r = M;
                g = z + m;
                b = m;
            }
            else if (h >= 60 && h < 120)
            {
                r = z + m;
                g = M;
                b = m;
            }
            else if (h >= 120 && h < 180)
            {
                r = m;
                g = M;
                b = z + m;
            }
            else if (h >= 180 && h < 240)
            {
                r = m;
                g = z+m;
                b = M;
            }
            else if (h >= 240 && h < 300)
            {
                r = z+m;
                g = m;
                b = M;
            }
            else if (h >= 300 && h < 360)
            {
                r = M;
                g = m;
                b = z + m;
            }

            return new Color(r, g, b);
        }


    }

    public class ColorPicker : Control
    {
        public ColorPicker()
        {
            this.DefaultStyleKey = typeof(ColorPicker);
        }






        public bool Blink
        {
            get { return (bool)GetValue(BlinkProperty); }
            set { SetValue(BlinkProperty, value); }
        }

        // Using a DependencyProperty enables animation, styling, binding, etc.
        public static readonly DependencyProperty BlinkProperty =
            DependencyProperty.Register(
                "Blink",                  // The name of the DependencyProperty
                typeof(bool),             // The type of the DependencyProperty
                typeof(ColorPicker),       // The type of the owner of the DependencyProperty
                new PropertyMetadata(     // OnBlinkChanged will be called when Blink changes
                    false,                // The default value of the DependencyProperty
                    new PropertyChangedCallback(OnBlinkChanged)
                )
            );

        private static void OnBlinkChanged(
            DependencyObject d,
            DependencyPropertyChangedEventArgs e
        )
        {
            var instance = d as ColorPicker;
            if (instance != null)
            {
                //do something on property change
            }
        }
    }

}
