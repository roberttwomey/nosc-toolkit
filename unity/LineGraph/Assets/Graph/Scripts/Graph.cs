using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Graph
{
    internal List<Line> lines;
    internal int number_of_channels;
    internal List<Color> colors = new List<Color>{new Color(89, 45, 45), new Color(255, 34, 0), new Color(89, 24, 0), new Color(191, 86, 48),
                                                  new Color(230, 187, 172), new Color(255, 179, 128), new Color(102, 66, 26), new Color(204, 136, 0),
                                                  new Color(115, 107, 0), new Color(77, 75, 57), new Color(230, 242, 61), new Color(188, 191, 143),
                                                  new Color(147, 191, 96), new Color(92, 230, 0), new Color(23, 51, 13), new Color(29, 115, 29),
                                                  new Color(0, 255, 170), new Color(89, 179, 149), new Color(45, 89, 80), new Color(0, 190, 204),
                                                  new Color(32, 57, 64), new Color(70, 117, 140), new Color(29, 63, 115), new Color(128, 179, 255) };

    public Graph(int number_of_channels, int point_Limit, float yMaximum)
    {
        lines = new List<Line>();
        Line init;

        for (int i=0; i < number_of_channels; i++){
            init = new Line(colors[i], i * yMaximum / number_of_channels, point_Limit);
            lines.Add(init);
        }

    }
}
