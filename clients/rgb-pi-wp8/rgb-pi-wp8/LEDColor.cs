using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Media;

namespace RGB
{
    public struct LEDColor
    {
        public float R, G, B;

        
        public LEDColor(float r, float g, float b)
        {
            R = r;
            G = g;
            B = b;
        }

        public LEDColor(Color color) : this(color.R, color.G, color.B)
        {            
        }

        public LEDColor(byte r, byte g, byte b)
        {
            R = r / 255.0f;
            G = g / 255.0f;
            B = b / 255.0f;
        }

        public LEDColor(string colorHex)
        {
            if (colorHex.Length == 3)
                colorHex = colorHex[0] + "" + colorHex[0] + colorHex[1] + "" + colorHex[1] + colorHex[2] + "" + colorHex[2];

            if (colorHex.Length != 6)
                throw new ArgumentException("strange lenght of hex color string: "+colorHex);

            byte r = Convert.ToByte(colorHex[0]+""+colorHex[1], 16);
            byte g = Convert.ToByte(colorHex[2]+""+colorHex[3], 16);
            byte b = Convert.ToByte(colorHex[4]+""+colorHex[5], 16);

            R = r / 255.0f;
            G = g / 255.0f;
            B = b / 255.0f;
        }


        public string ToString(string format)
        {
            switch (format)
            {
                case "f": return ToString();
                case "b": return "{b:" + ((byte)(R * 255)) + "," + ((byte)(G * 255)) + "," + ((byte)(B * 255)) + "}";
                case "x": return "{x:" + ((byte)(R * 255)).ToString("X2") + ((byte)(G * 255)).ToString("X2") + ((byte)(B * 255)).ToString("X2") + "}";
            }

            throw new ArgumentException("unknown color format: " + format + "  allowed are only {f, b, x}");
        }

        public override string ToString()
        {
            return "{f:" + R.ToString("F3").Replace(',', '.') + "," + G.ToString("F3").Replace(',', '.') + "," + B.ToString("F3").Replace(',', '.') + "}";
        }

    }
}
